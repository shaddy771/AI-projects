"""Поиск и (опционально) скачивание изображений для объявлений."""

from __future__ import annotations

import hashlib
import logging
import re
from pathlib import Path
from urllib.parse import urlparse

import requests

logger = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (compatible; AvitoListingsAgent/0.1; +https://github.com/)"
)


def search_image_urls(
    query: str,
    *,
    limit: int = 3,
    source: str = "duckduckgo",
) -> list[str]:
    query = query.strip()
    if not query:
        return []
    if source == "duckduckgo":
        return _search_duckduckgo(query, limit=limit)
    raise ValueError(f"Неизвестный image_source: {source}")


def _search_duckduckgo(query: str, *, limit: int) -> list[str]:
    try:
        from ddgs import DDGS
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "Пакет ddgs не установлен. Выполните: pip install -r requirements.txt"
        ) from exc

    urls: list[str] = []
    seen: set[str] = set()
    try:
        with DDGS() as ddgs:
            results = ddgs.images(
                query,
                max_results=max(limit * 3, 10),
                safesearch="moderate",
            )
            for item in results:
                url = (item.get("image") or item.get("url") or "").strip()
                if not url or not url.startswith(("http://", "https://")):
                    continue
                if _looks_like_page(url):
                    continue
                if url in seen:
                    continue
                seen.add(url)
                urls.append(url)
                if len(urls) >= limit:
                    break
    except Exception as exc:  # noqa: BLE001
        logger.warning("Поиск картинок не удался для %r: %s", query, exc)
    return urls


def _looks_like_page(url: str) -> bool:
    path = urlparse(url).path.lower()
    if any(path.endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".webp", ".gif")):
        return False
    # часто в выдаче встречаются страницы-обёртки
    host = urlparse(url).netloc.lower()
    if any(bad in host for bad in ("pinterest.", "facebook.", "instagram.")):
        return True
    return False


def download_images(
    urls: list[str],
    dest_dir: Path,
    *,
    prefix: str,
) -> list[Path]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []
    for index, url in enumerate(urls, start=1):
        try:
            path = _download_one(url, dest_dir, prefix=f"{prefix}_{index:02d}")
            if path:
                saved.append(path)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Не удалось скачать %s: %s", url, exc)
    return saved


def _download_one(url: str, dest_dir: Path, *, prefix: str) -> Path | None:
    response = requests.get(
        url,
        timeout=30,
        headers={"User-Agent": USER_AGENT},
        stream=True,
    )
    response.raise_for_status()
    content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
    ext = _ext_from_content_type(content_type) or _ext_from_url(url) or ".jpg"
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    filename = f"{_safe_name(prefix)}_{digest}{ext}"
    path = dest_dir / filename
    with path.open("wb") as fh:
        for chunk in response.iter_content(chunk_size=65536):
            if chunk:
                fh.write(chunk)
    if path.stat().st_size < 1024:
        path.unlink(missing_ok=True)
        return None
    return path


def _ext_from_content_type(content_type: str) -> str | None:
    mapping = {
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "image/gif": ".gif",
    }
    return mapping.get(content_type.lower())


def _ext_from_url(url: str) -> str | None:
    path = urlparse(url).path.lower()
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
        if path.endswith(ext):
            return ".jpg" if ext == ".jpeg" else ext
    return None


def _safe_name(value: str) -> str:
    value = re.sub(r"[^\w\-]+", "_", value, flags=re.UNICODE)
    return value.strip("_")[:60] or "img"


def join_image_urls(urls: list[str]) -> str:
    """Авито принимает разделитель | или перевод строки."""
    return "|".join(u.strip() for u in urls if u.strip())
