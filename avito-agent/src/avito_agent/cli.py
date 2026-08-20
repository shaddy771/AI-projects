"""CLI агента объявлений Авито."""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from .loaders import load_products, load_seller_config
from .pipeline import build_listings
from .xlsx_writer import write_xlsx

console = Console()


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Подробные логи")
def main(verbose: bool) -> None:
    """Агент: описания + картинки + XLSX для автозагрузки Авито."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s %(name)s: %(message)s")


@main.command("generate")
@click.option(
    "--products",
    "products_path",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="YAML/JSON/CSV со списком товаров",
)
@click.option(
    "--config",
    "config_path",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="YAML/JSON с реквизитами продавца",
)
@click.option(
    "--output",
    "output_path",
    type=click.Path(path_type=Path),
    default=Path("workspace/output/avito_listings.xlsx"),
    show_default=True,
)
@click.option("--no-images", is_flag=True, help="Не искать картинки")
@click.option("--download-images", is_flag=True, help="Скачать найденные фото локально")
@click.option(
    "--images-dir",
    type=click.Path(path_type=Path),
    default=Path("workspace/images"),
    show_default=True,
)
@click.option("--images-per-item", type=int, default=None, help="Сколько фото на товар")
@click.option("--sheet-name", default="Объявления", show_default=True)
def generate_cmd(
    products_path: Path,
    config_path: Path,
    output_path: Path,
    no_images: bool,
    download_images: bool,
    images_dir: Path,
    images_per_item: int | None,
    sheet_name: str,
) -> None:
    """Собрать XLSX с описаниями и ссылками на фото."""
    seller = load_seller_config(config_path)
    if download_images:
        seller.download_images = True
    products = load_products(products_path)
    if not products:
        console.print("[red]Список товаров пуст[/red]")
        sys.exit(1)

    result = build_listings(
        products,
        seller,
        search_images=not no_images,
        images_dir=images_dir,
        images_per_item=images_per_item,
    )
    path = write_xlsx(result.rows, output_path, sheet_name=sheet_name)
    result.output_xlsx = path

    table = Table(title="Готовые объявления")
    table.add_column("Id")
    table.add_column("Title")
    table.add_column("Price")
    table.add_column("Photos")
    for row in result.rows:
        n_photos = 0
        if row.ImageUrls:
            n_photos = len([u for u in row.ImageUrls.split("|") if u.strip()])
        elif row.ImageNames:
            n_photos = len([u for u in row.ImageNames.split("|") if u.strip()])
        table.add_row(row.Id, row.Title, str(row.Price or ""), str(n_photos))
    console.print(table)

    for warning in result.warnings:
        console.print(f"[yellow]⚠ {warning}[/yellow]")

    console.print(f"[green]XLSX сохранён:[/green] {path.resolve()}")
    _write_sidecar_report(path, result.warnings)


@main.command("search-images")
@click.argument("query")
@click.option("--limit", default=5, show_default=True)
@click.option("--download/--no-download", default=False)
@click.option(
    "--out-dir",
    type=click.Path(path_type=Path),
    default=Path("workspace/images/manual"),
)
def search_images_cmd(query: str, limit: int, download: bool, out_dir: Path) -> None:
    """Найти картинки по текстовому запросу."""
    from .images import download_images, search_image_urls

    urls = search_image_urls(query, limit=limit)
    if not urls:
        console.print("[red]Ничего не найдено[/red]")
        sys.exit(2)
    for url in urls:
        console.print(url)
    if download:
        paths = download_images(urls, out_dir, prefix="manual")
        console.print(f"Скачано файлов: {len(paths)} → {out_dir}")


@main.command("validate")
@click.option(
    "--products",
    "products_path",
    type=click.Path(exists=True, path_type=Path),
    required=True,
)
@click.option(
    "--config",
    "config_path",
    type=click.Path(exists=True, path_type=Path),
    required=True,
)
def validate_cmd(products_path: Path, config_path: Path) -> None:
    """Проверить входные данные до генерации (без поиска картинок)."""
    from .categories import DESCRIPTION_MAX_LEN, TITLE_MAX_LEN
    from .descriptions import build_description, build_title

    seller = load_seller_config(config_path)
    products = load_products(products_path)
    errors: list[str] = []
    for p in products:
        if not p.id:
            errors.append("Товар без Id")
        title = build_title(p)
        if len(title) > TITLE_MAX_LEN:
            errors.append(f"[{p.id}] Title > {TITLE_MAX_LEN}")
        desc = build_description(p, seller)
        if len(desc) > DESCRIPTION_MAX_LEN:
            errors.append(f"[{p.id}] Description > {DESCRIPTION_MAX_LEN}")
        if p.price is not None and float(p.price) < 0:
            errors.append(f"[{p.id}] отрицательная цена")
    if not seller.address:
        errors.append("В конфиге нет address")
    if not seller.contact_phone:
        errors.append("В конфиге нет contact_phone")

    if errors:
        for e in errors:
            console.print(f"[red]• {e}[/red]")
        sys.exit(1)
    console.print(f"[green]OK[/green]: {len(products)} товаров, конфиг продавца валиден")


def _write_sidecar_report(xlsx_path: Path, warnings: list[str]) -> None:
    report = {
        "xlsx": str(xlsx_path),
        "warnings": warnings,
        "next_steps": [
            "Сверьте колонки с шаблоном категории в кабинете Авито",
            "Убедитесь, что ImageUrls открываются без авторизации",
            "Загрузите файл в Автозагрузку или проверьте XML-эквивалент",
            "Смотрите чеклист: avito-agent/checklists/full-placement.md",
        ],
    }
    side = xlsx_path.with_suffix(".report.json")
    side.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
