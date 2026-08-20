"""Загрузка входных товаров и конфига продавца."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import yaml

from .models import ProductInput, SellerConfig


def load_seller_config(path: Path) -> SellerConfig:
    data = _load_structured(path)
    if "seller" in data and isinstance(data["seller"], dict):
        data = data["seller"]
    return SellerConfig.model_validate(data)


def load_products(path: Path) -> list[ProductInput]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return _load_products_csv(path)
    data = _load_structured(path)
    if isinstance(data, dict):
        items = data.get("products") or data.get("items") or data.get("ads")
        if items is None:
            raise ValueError(f"В {path} ожидается ключ products/items/ads")
    elif isinstance(data, list):
        items = data
    else:
        raise ValueError(f"Неподдерживаемый формат: {path}")
    return [ProductInput.model_validate(_normalize_item(item)) for item in items]


def _load_structured(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    if suffix == ".json":
        return json.loads(text)
    raise ValueError(f"Ожидался YAML/JSON: {path}")


def _load_products_csv(path: Path) -> list[ProductInput]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        items = []
        for row in reader:
            cleaned = {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items() if k}
            if cleaned.get("features"):
                cleaned["features"] = _split_list(cleaned["features"])
            if cleaned.get("keywords"):
                cleaned["keywords"] = _split_list(cleaned["keywords"])
            if cleaned.get("image_urls"):
                cleaned["image_urls"] = _split_list(cleaned["image_urls"], seps="|;,")
            items.append(ProductInput.model_validate(_normalize_item(cleaned)))
        return items


def _normalize_item(item: dict[str, Any]) -> dict[str, Any]:
    mapping = {
        "Id": "id",
        "Title": "title",
        "Name": "name",
        "Brand": "brand",
        "Model": "model",
        "Category": "category",
        "GoodsType": "goods_type",
        "ProductType": "product_type",
        "Price": "price",
        "Condition": "condition",
        "Description": "description",
        "ImageUrls": "image_urls",
        "ImageQuery": "image_query",
    }
    out: dict[str, Any] = {}
    extras: dict[str, Any] = {}
    known = set(ProductInput.model_fields)
    for key, value in item.items():
        if value is None or value == "":
            continue
        norm = mapping.get(key, key)
        norm = norm[0].lower() + norm[1:] if norm[:1].isupper() and norm not in mapping.values() else norm
        # snake from camel
        if norm not in known and key not in known:
            snake = _to_snake(key)
            if snake in known:
                out[snake] = value
            elif key in {"extras"} and isinstance(value, dict):
                extras.update(value)
            else:
                extras[key] = value
        else:
            out[norm if norm in known else key] = value
    if extras:
        out["extras"] = {**out.get("extras", {}), **extras}
    return out


def _to_snake(name: str) -> str:
    out = []
    for i, ch in enumerate(name):
        if ch.isupper() and i > 0:
            out.append("_")
            out.append(ch.lower())
        else:
            out.append(ch.lower())
    return "".join(out)


def _split_list(value: str, seps: str = "|;,") -> list[str]:
    for sep in seps:
        if sep in value:
            return [p.strip() for p in value.split(sep) if p.strip()]
    return [value.strip()] if value.strip() else []
