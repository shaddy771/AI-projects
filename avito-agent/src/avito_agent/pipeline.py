"""Пайплайн: товары → описания → картинки → XLSX."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from .categories import resolve_category_preset
from .descriptions import build_description, build_title
from .images import download_images, join_image_urls, search_image_urls
from .models import ListingRow, ProductInput, SellerConfig

logger = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    rows: list[ListingRow]
    output_xlsx: Path | None = None
    image_files: dict[str, list[Path]] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


def build_listings(
    products: list[ProductInput],
    seller: SellerConfig,
    *,
    search_images: bool = True,
    images_dir: Path | None = None,
    images_per_item: int | None = None,
) -> PipelineResult:
    limit = images_per_item if images_per_item is not None else seller.images_per_item
    warnings: list[str] = []
    rows: list[ListingRow] = []
    image_files: dict[str, list[Path]] = {}

    for product in products:
        title = build_title(product)
        description = build_description(product, seller)
        category = product.category or seller.default_category
        goods_type = product.goods_type or seller.default_goods_type
        product_type = product.product_type

        # если category — ключ пресета
        if category.lower() in {"home", "electronics", "phones", "clothes", "auto_parts", "hobby", "kids", "beauty"}:
            preset = resolve_category_preset(category)
            category = str(preset["Category"])
            goods_type = goods_type or preset.get("GoodsType")
            product_type = product_type or preset.get("ProductType")

        urls = list(product.image_urls)
        names = list(product.image_names)

        if search_images and len(urls) < limit and not names:
            needed = limit - len(urls)
            found = search_image_urls(
                product.search_query(),
                limit=needed,
                source=seller.image_source,
            )
            if not found:
                warnings.append(
                    f"[{product.id}] не найдены картинки по запросу «{product.search_query()}»"
                )
            urls.extend(found)

        if seller.download_images and urls and images_dir is not None:
            saved = download_images(urls, images_dir / product.id, prefix=product.id)
            image_files[product.id] = saved
            if seller.image_host_base_url:
                base = seller.image_host_base_url.rstrip("/")
                urls = [f"{base}/{product.id}/{p.name}" for p in saved]
                names = []
            else:
                # для загрузки архивом — имена файлов
                names = [p.name for p in saved]
                # URL оставляем как fallback, если хостинг не настроен
                if not seller.image_host_base_url:
                    warnings.append(
                        f"[{product.id}] фото скачаны локально; для ImageUrls нужен публичный хостинг "
                        f"(image_host_base_url) или загрузка zip с ImageNames"
                    )

        price = product.price
        if price is not None:
            price = int(round(float(price)))

        extras = {**seller.extra_defaults, **product.extras}
        row = ListingRow(
            Id=str(product.id),
            Category=category,
            Title=title,
            Description=description,
            Price=price,
            ImageUrls=join_image_urls(urls) if not names or seller.image_host_base_url else "",
            ImageNames="|".join(names),
            Address=product.address or seller.address,
            ContactPhone=product.contact_phone or seller.contact_phone,
            ManagerName=product.manager_name or seller.manager_name,
            ContactMethod=seller.contact_method,
            AdType=product.ad_type or seller.default_ad_type,
            Condition=product.condition or seller.default_condition,
            Availability=product.availability or seller.default_availability,
            GoodsType=goods_type,
            ProductType=product_type,
            ListingFee=seller.listing_fee,
            extras=extras,
        )
        # если есть и URL, и не хотим терять найденные ссылки при локальном скачивании без хостинга
        if urls and not row.ImageUrls and not names:
            row.ImageUrls = join_image_urls(urls)
        elif urls and names and not seller.image_host_base_url:
            # дублируем URL — удобно для ручной проверки до загрузки zip
            row.ImageUrls = join_image_urls(urls)

        rows.append(row)

    return PipelineResult(rows=rows, image_files=image_files, warnings=warnings)
