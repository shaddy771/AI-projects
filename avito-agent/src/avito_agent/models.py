from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator


class SellerConfig(BaseModel):
    """Общие реквизиты продавца для всех объявлений."""

    address: str = Field(..., description="Полный адрес как на Авито")
    contact_phone: str = Field(..., description="Телефон в формате +7...")
    manager_name: str = "Менеджер"
    contact_method: str = "По телефону и в сообщениях"
    listing_fee: str = "Package"
    default_category: str = "Товары для дома и дачи"
    default_goods_type: str | None = None
    default_condition: str = "Новое"
    default_ad_type: str = "Товар приобретен на продажу"
    default_availability: str = "В наличии"
    description_style: str = "avito_sales"
    images_per_item: int = 3
    image_source: str = "duckduckgo"
    download_images: bool = False
    image_host_base_url: str | None = None
    extra_defaults: dict[str, Any] = Field(default_factory=dict)


class ProductInput(BaseModel):
    """Входная карточка товара (минимум для генерации)."""

    id: str
    title: str | None = None
    name: str | None = None
    brand: str | None = None
    model: str | None = None
    category: str | None = None
    goods_type: str | None = None
    product_type: str | None = None
    price: int | float | None = None
    condition: str | None = None
    ad_type: str | None = None
    availability: str | None = None
    address: str | None = None
    contact_phone: str | None = None
    manager_name: str | None = None
    description: str | None = None
    features: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    image_query: str | None = None
    image_urls: list[str] = Field(default_factory=list)
    image_names: list[str] = Field(default_factory=list)
    extras: dict[str, Any] = Field(default_factory=dict)

    @field_validator("price", mode="before")
    @classmethod
    def _clean_price(cls, value: Any) -> int | float | None:
        if value is None or value == "":
            return None
        if isinstance(value, (int, float)):
            return value
        text = str(value).replace(" ", "").replace("₽", "").replace("руб.", "").replace("руб", "")
        text = text.replace(",", ".")
        return float(text) if "." in text else int(text)

    def display_name(self) -> str:
        if self.title:
            return self.title.strip()
        parts = [p for p in [self.brand, self.name or self.model] if p]
        if parts:
            return " ".join(parts)
        return self.id

    def search_query(self) -> str:
        if self.image_query:
            return self.image_query
        bits = [self.brand, self.name or self.model or self.title]
        bits.extend(self.keywords[:3])
        return " ".join(b for b in bits if b).strip() or self.display_name()


class ListingRow(BaseModel):
    """Готовая строка для листа автозагрузки Авито."""

    Id: str
    Category: str
    Title: str
    Description: str
    Price: int | None = None
    ImageUrls: str = ""
    ImageNames: str = ""
    Address: str
    ContactPhone: str
    ManagerName: str = "Менеджер"
    ContactMethod: str = "По телефону и в сообщениях"
    AdType: str = "Товар приобретен на продажу"
    Condition: str = "Новое"
    Availability: str = "В наличии"
    GoodsType: str | None = None
    ProductType: str | None = None
    ListingFee: str = "Package"
    AvitoId: str = ""
    VideoURL: str = ""
    extras: dict[str, Any] = Field(default_factory=dict)

    def to_sheet_dict(self) -> dict[str, Any]:
        base = {
            "Id": self.Id,
            "AvitoId": self.AvitoId,
            "Category": self.Category,
            "GoodsType": self.GoodsType or "",
            "ProductType": self.ProductType or "",
            "Title": self.Title,
            "Description": self.Description,
            "Price": self.Price if self.Price is not None else "",
            "ImageUrls": self.ImageUrls,
            "ImageNames": self.ImageNames,
            "VideoURL": self.VideoURL,
            "Address": self.Address,
            "ContactPhone": self.ContactPhone,
            "ManagerName": self.ManagerName,
            "ContactMethod": self.ContactMethod,
            "AdType": self.AdType,
            "Condition": self.Condition,
            "Availability": self.Availability,
            "ListingFee": self.ListingFee,
        }
        for key, value in self.extras.items():
            if key not in base:
                base[key] = value
        return base
