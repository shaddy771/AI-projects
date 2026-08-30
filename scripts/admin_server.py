#!/usr/bin/env python3
"""Flask admin panel for blog article management."""

import hashlib
import json
import subprocess
import sys
from datetime import date
from functools import wraps
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory, session

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from articles import (  # noqa: E402
    ARTICLES_FILE,
    load_articles,
    published_articles,
    save_articles,
    scheduled_articles,
)

CONFIG_FILE = ROOT / "data" / "admin-config.json"
DEFAULT_PASSWORD = "zamok2026"

app = Flask(__name__, static_folder=str(ROOT / "admin"), static_url_path="/admin")
app.secret_key = "zamok-admin-secret-change-in-production"


def load_config() -> dict:
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    cfg = {"password_hash": hash_password(DEFAULT_PASSWORD)}
    CONFIG_FILE.parent.mkdir(exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    return cfg


def hash_password(pwd: str) -> str:
    return hashlib.sha256(pwd.encode()).hexdigest()


def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("authenticated"):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapper


@app.route("/")
def root():
    return send_from_directory(ROOT / "admin", "index.html")


@app.route("/admin/")
@app.route("/admin")
def admin_page():
    return send_from_directory(ROOT / "admin", "index.html")


@app.route("/admin/<path:path>")
def admin_static(path):
    return send_from_directory(ROOT / "admin", path)


@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    pwd = data.get("password", "")
    cfg = load_config()
    if hash_password(pwd) == cfg["password_hash"]:
        session["authenticated"] = True
        return jsonify({"ok": True})
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
    for a in load_articles():
        if a["slug"] == slug:
            return jsonify(a)
    return jsonify({"error": "Not found"}), 404


@app.patch("/api/articles/<slug>")
@auth_required
def update_article(slug):
    data = request.get_json(silent=True) or {}
    articles = load_articles()
    for i, a in enumerate(articles):
        if a["slug"] == slug:
            for key in ("title", "desc", "content", "keywords", "date", "status", "img"):
                if key in data:
                    articles[i][key] = data[key]
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
    )
    return jsonify({
        "ok": result.returncode == 0,
        "output": result.stdout + result.stderr,
    })


@app.post("/api/seed")
@auth_required
def seed():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "seed_articles.py")],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    return jsonify({
        "ok": result.returncode == 0,
        "output": result.stdout + result.stderr,
    })


if __name__ == "__main__":
    load_config()
    print(f"Admin: http://127.0.0.1:8787/admin/")
    print(f"Password (default): {DEFAULT_PASSWORD}")
    app.run(host="0.0.0.0", port=8787, debug=False)
