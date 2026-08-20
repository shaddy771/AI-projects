"""Генерация заголовков и описаний под Авито."""

from __future__ import annotations

import re
from textwrap import dedent

from .categories import DESCRIPTION_MAX_LEN, TITLE_MAX_LEN
from .models import ProductInput, SellerConfig


def _clip(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def build_title(product: ProductInput) -> str:
    raw = product.display_name()
    # Авито: без КАПСА, без лишних символов, до ~50 символов
    raw = re.sub(r"[!?]{2,}", "!", raw)
    raw = re.sub(r"[A-ZА-Я]{8,}", lambda m: m.group(0).title(), raw)
    return _clip(raw, TITLE_MAX_LEN)


def build_description(product: ProductInput, seller: SellerConfig) -> str:
    if product.description and product.description.strip():
        return _clip_html(product.description.strip(), DESCRIPTION_MAX_LEN)

    name = product.display_name()
    brand = product.brand or ""
    features = product.features or []
    condition = product.condition or seller.default_condition
    availability = product.availability or seller.default_availability

    feature_block = ""
    if features:
        items = "\n".join(f"<li>{_escape(f)}</li>" for f in features)
        feature_block = f"<p><strong>Характеристики:</strong></p><ul>{items}</ul>"

    brand_line = f"<p>Бренд: {_escape(brand)}</p>" if brand else ""

    body = dedent(
        f"""
        <p><strong>{_escape(name)}</strong></p>
        {brand_line}
        <p>Состояние: {_escape(condition)}. Наличие: {_escape(availability)}.</p>
        {feature_block}
        <p>Товар готов к отправке/самовывозу. Ответим на вопросы в сообщениях Авито
        или по телефону. Возможен торг при осмотре.</p>
        <p>Пишите, если нужны дополнительные фото или уточнения по комплектации.</p>
        """
    ).strip()
    return _clip_html(body, DESCRIPTION_MAX_LEN)


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _clip_html(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    # грубое обрезание с сохранением читаемости
    truncated = text[: limit - 20]
    # закрываем незакрытые простые теги приблизительно
    for tag in ("ul", "li", "p", "strong"):
        opens = truncated.count(f"<{tag}>") + truncated.count(f"<{tag} ")
        closes = truncated.count(f"</{tag}>")
        if opens > closes:
            truncated += f"</{tag}>" * (opens - closes)
    return truncated
