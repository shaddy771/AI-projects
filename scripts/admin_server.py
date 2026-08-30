#!/usr/bin/env python3
"""Flask admin panel for blog article management."""

import hashlib
import hmac
import json
import os
import re
import secrets
import subprocess
import sys
import time
from datetime import date
from functools import wraps
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory, session

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from articles import (  # noqa: E402
    load_articles,
    published_articles,
    save_articles,
    scheduled_articles,
)

CONFIG_FILE = ROOT / "data" / "admin-config.json"
ALLOWED_IMAGES = {"door-unlock", "car-unlock", "lock-repair", "master-work"}
ALLOWED_STATUS = {"scheduled", "published", "draft"}
ALLOWED_HTML_TAGS = {
    "p", "h2", "h3", "h4", "ul", "ol", "li", "a", "strong", "em", "b", "i",
    "br", "blockquote", "figure", "figcaption", "img",
}
ALLOWED_HTML_ATTRS = {
    "a": ["href", "title", "rel"],
    "img": ["src", "alt", "width", "height", "loading", "decoding"],
}
LOGIN_ATTEMPTS: dict[str, list[float]] = {}
MAX_LOGIN_ATTEMPTS = 5
LOGIN_WINDOW_SEC = 300

app = Flask(__name__, static_folder=str(ROOT / "admin"), static_url_path="/admin")
app.config.update(
    SECRET_KEY=os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("ADMIN_HTTPS", "").lower() in ("1", "true", "yes"),
    PERMANENT_SESSION_LIFETIME=3600 * 8,
)


def hash_password(pwd: str, salt: str | None = None) -> str:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", pwd.encode(), salt.encode(), 120_000).hex()
    return f"{salt}${digest}"


def verify_password(pwd: str, stored: str) -> bool:
    try:
        salt, digest = stored.split("$", 1)
    except ValueError:
        # Legacy unsalted SHA256 hashes from older configs.
        return hmac.compare_digest(hashlib.sha256(pwd.encode()).hexdigest(), stored)
    check = hashlib.pbkdf2_hmac("sha256", pwd.encode(), salt.encode(), 120_000).hex()
    return hmac.compare_digest(check, digest)


def load_config() -> dict:
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    initial_pwd = os.environ.get("ADMIN_PASSWORD")
    if not initial_pwd:
        initial_pwd = secrets.token_urlsafe(12)
        print("WARNING: ADMIN_PASSWORD not set. Generated one-time password:")
        print(initial_pwd)
        print("Set ADMIN_PASSWORD env var and restart to keep a fixed password.")
    cfg = {"password_hash": hash_password(initial_pwd)}
    CONFIG_FILE.parent.mkdir(exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    return cfg


def sanitize_html(html: str) -> str:
    try:
        import bleach
    except ImportError:
        return html
    return bleach.clean(
        html,
        tags=list(ALLOWED_HTML_TAGS),
        attributes=ALLOWED_HTML_ATTRS,
        strip=True,
    )


def client_ip() -> str:
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr or "unknown"


def login_blocked(ip: str) -> bool:
    now = time.time()
    attempts = [t for t in LOGIN_ATTEMPTS.get(ip, []) if now - t < LOGIN_WINDOW_SEC]
    LOGIN_ATTEMPTS[ip] = attempts
    return len(attempts) >= MAX_LOGIN_ATTEMPTS


def record_failed_login(ip: str) -> None:
    LOGIN_ATTEMPTS.setdefault(ip, []).append(time.time())


def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("authenticated"):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapper


@app.after_request
def security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.route("/")
def root():
    return send_from_directory(ROOT / "admin", "index.html")


@app.route("/admin/")
@app.route("/admin")
def admin_page():
    return send_from_directory(ROOT / "admin", "index.html")


@app.route("/admin/<path:path>")
def admin_static(path):
    if path.startswith(".") or ".." in path:
        return jsonify({"error": "Forbidden"}), 403
    return send_from_directory(ROOT / "admin", path)


@app.post("/api/login")
def login():
    ip = client_ip()
    if login_blocked(ip):
        return jsonify({"error": "Слишком много попыток. Подождите 5 минут."}), 429
    data = request.get_json(silent=True) or {}
    pwd = data.get("password", "")
    cfg = load_config()
    if verify_password(pwd, cfg["password_hash"]):
        session.clear()
        session["authenticated"] = True
        session.permanent = True
        LOGIN_ATTEMPTS.pop(ip, None)
        return jsonify({"ok": True})
    record_failed_login(ip)
    return jsonify({"error": "Неверный пароль"}), 401


@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})


@app.get("/api/stats")
@auth_required
def stats():
    articles = load_articles()
    today = date.today()
    pub = published_articles(today)
    sched = scheduled_articles(today)
    return jsonify({
        "total": len(articles),
        "published": len(pub),
        "scheduled": len(sched),
        "today": today.isoformat(),
        "next_publish": sched[0]["date"] if sched else None,
        "next_title": sched[0]["title"][:60] if sched else None,
    })


@app.get("/api/articles")
@auth_required
def list_articles():
    articles = load_articles()
    today = date.today()
    brief = []
    for a in sorted(articles, key=lambda x: x["date"], reverse=True):
        st = a.get("status", "scheduled")
        pub = a["date"] <= today.isoformat() and st != "draft"
        brief.append({
            "slug": a["slug"],
            "title": a["title"],
            "date": a["date"],
            "status": "published" if pub else st,
            "img": a.get("img", ""),
            "city": a.get("city"),
        })
    return jsonify(brief)


@app.get("/api/articles/<slug>")
@auth_required
def get_article(slug):
    if not SLUG_RE.match(slug):
        return jsonify({"error": "Invalid slug"}), 400
    for a in load_articles():
        if a["slug"] == slug:
            return jsonify(a)
    return jsonify({"error": "Not found"}), 404


@app.patch("/api/articles/<slug>")
@auth_required
def update_article(slug):
    if not SLUG_RE.match(slug):
        return jsonify({"error": "Invalid slug"}), 400
    data = request.get_json(silent=True) or {}
    articles = load_articles()
    for i, a in enumerate(articles):
        if a["slug"] == slug:
            for key in ("title", "desc", "content", "keywords", "date", "status", "img"):
                if key not in data:
                    continue
                value = data[key]
                if key == "content":
                    value = sanitize_html(str(value))[:50000]
                elif key == "status":
                    value = str(value)
                    if value not in ALLOWED_STATUS:
                        return jsonify({"error": "Invalid status"}), 400
                elif key == "img":
                    value = str(value)
                    if value not in ALLOWED_IMAGES:
                        return jsonify({"error": "Invalid image"}), 400
                elif key == "date":
                    value = str(value)[:10]
                else:
                    value = str(value)[:2000]
                articles[i][key] = value
            save_articles(articles)
            return jsonify({"ok": True})
    return jsonify({"error": "Not found"}), 404


@app.post("/api/rebuild")
@auth_required
def rebuild():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "generate_pages.py")],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    output = (result.stdout + result.stderr)[-4000:]
    return jsonify({
        "ok": result.returncode == 0,
        "output": output,
    })


@app.post("/api/seed")
@auth_required
def seed():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "seed_articles.py")],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    output = (result.stdout + result.stderr)[-4000:]
    return jsonify({
        "ok": result.returncode == 0,
        "output": output,
    })


if __name__ == "__main__":
    load_config()
    host = os.environ.get("ADMIN_HOST", "127.0.0.1")
    port = int(os.environ.get("ADMIN_PORT", "8787"))
    print(f"Admin panel: http://{host}:{port}/admin/")
    if host == "0.0.0.0":
        print("WARNING: Admin listens on all interfaces. Use only behind VPN or with HTTPS + firewall.")
    app.run(host=host, port=port, debug=False)
