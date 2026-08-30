#!/usr/bin/env python3
"""Article storage, scheduling and publishing helpers."""

import json
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTICLES_FILE = ROOT / "data" / "articles.json"
BLOG_PER_PAGE = 12


def load_articles() -> list[dict]:
    if not ARTICLES_FILE.exists():
        return []
    return json.loads(ARTICLES_FILE.read_text(encoding="utf-8"))


def save_articles(articles: list[dict]) -> None:
    ARTICLES_FILE.parent.mkdir(exist_ok=True)
    ARTICLES_FILE.write_text(
        json.dumps(articles, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def parse_date(value: str) -> date:
    return datetime.strptime(value[:10], "%Y-%m-%d").date()


def is_published(article: dict, as_of: date | None = None) -> bool:
    as_of = as_of or date.today()
    if article.get("status") == "draft":
        return False
    if article.get("status") == "published":
        return True
    return parse_date(article["date"]) <= as_of


def published_articles(as_of: date | None = None) -> list[dict]:
    items = [a for a in load_articles() if is_published(a, as_of)]
    return sorted(items, key=lambda a: a["date"], reverse=True)


def scheduled_articles(as_of: date | None = None) -> list[dict]:
    as_of = as_of or date.today()
    items = [
        a for a in load_articles()
        if a.get("status", "scheduled") == "scheduled" and parse_date(a["date"]) > as_of
    ]
    return sorted(items, key=lambda a: a["date"])


def paginate_articles(articles: list[dict], page: int, per_page: int = BLOG_PER_PAGE) -> tuple[list[dict], int]:
    total_pages = max(1, (len(articles) + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    return articles[start : start + per_page], total_pages


def article_by_slug(slug: str) -> dict | None:
    for a in load_articles():
        if a["slug"] == slug:
            return a
    return None
