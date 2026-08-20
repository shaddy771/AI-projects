"""Шаблоны категорий и допустимые значения для товаров Авито."""

from __future__ import annotations

# Базовые колонки, общие для большинства товарных категорий.
# Итоговый шаблон категории всегда лучше брать из кабинета Авито:
# https://autoload.avito.ru/format/
COMMON_COLUMNS: list[str] = [
    "Id",
    "AvitoId",
    "Category",
    "GoodsType",
    "ProductType",
    "Title",
    "Description",
    "Price",
    "ImageUrls",
    "ImageNames",
    "VideoURL",
    "Address",
    "ContactPhone",
    "ManagerName",
    "ContactMethod",
    "AdType",
    "Condition",
    "Availability",
    "ListingFee",
]

CATEGORY_PRESETS: dict[str, dict[str, str | None]] = {
    "home": {
        "Category": "Товары для дома и дачи",
        "GoodsType": "Мебель и интерьер",
        "ProductType": None,
    },
    "electronics": {
        "Category": "Бытовая электроника",
        "GoodsType": None,
        "ProductType": None,
    },
    "phones": {
        "Category": "Телефоны",
        "GoodsType": "Мобильные телефоны",
        "ProductType": None,
    },
    "clothes": {
        "Category": "Одежда, обувь, аксессуары",
        "GoodsType": "Женская одежда",
        "ProductType": None,
    },
    "auto_parts": {
        "Category": "Запчасти и аксессуары",
        "GoodsType": "Для автомобилей",
        "ProductType": None,
    },
    "hobby": {
        "Category": "Хобби и отдых",
        "GoodsType": None,
        "ProductType": None,
    },
    "kids": {
        "Category": "Товары для детей и игрушки",
        "GoodsType": None,
        "ProductType": None,
    },
    "beauty": {
        "Category": "Красота и здоровье",
        "GoodsType": None,
        "ProductType": None,
    },
}

# Ограничения Авито (ориентиры; актуальные лимиты — в справке категории).
TITLE_MAX_LEN = 50
DESCRIPTION_MAX_LEN = 7500
ADDRESS_MAX_LEN = 256

AD_TYPES = [
    "Товар приобретен на продажу",
    "Товар от производителя",
]

CONDITIONS = ["Новое", "Б/у"]

CONTACT_METHODS = [
    "По телефону и в сообщениях",
    "По телефону",
    "В сообщениях",
]

LISTING_FEES = ["Package", "PackageSingle", "Single"]


def resolve_category_preset(key: str | None) -> dict[str, str | None]:
    if not key:
        return CATEGORY_PRESETS["home"]
    return CATEGORY_PRESETS.get(key.lower(), CATEGORY_PRESETS["home"])
