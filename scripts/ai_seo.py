#!/usr/bin/env python3
"""Generate llms.txt files for AI search engines."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from generate_pages import CITIES  # noqa: E402
from articles import published_articles  # noqa: E402
from shared import (  # noqa: E402
    BLOG_POSTS,
    DOMAIN,
    EMAIL,
    PHONE,
    PHONE_TEL,
    SERVICE_COMBOS,
    TELEGRAM_URL,
    WHATSAPP_URL,
    VIBER_URL,
)

FAQ_GLOBAL = [
    ("Сколько стоит вскрытие замка в Могилёве?", "От 30 BYN. Точная цена зависит от типа замка и времени вызова."),
    ("Как быстро приедет мастер?", "По Могилёву — 15–20 минут. По области — от 30 до 60 минут."),
    ("Можно ли вскрыть замок без повреждений?", "Да, в 95% случаев без повреждения двери и механизма."),
    ("Работаете ли вы ночью?", "Да, круглосуточно 7 дней в неделю, включая праздники."),
    ("Какие документы нужны?", "Для квартиры — документ на жильё. Для авто — документы на ТС и паспорт."),
]

PRICES = [
    ("Вскрытие входной двери (цилиндр)", "от 35 BYN"),
    ("Вскрытие сувальдного замка", "от 45 BYN"),
    ("Вскрытие автомобиля", "от 40 BYN"),
    ("Вскрытие сейфа", "от 60 BYN"),
    ("Замена личинки", "от 25 BYN"),
    ("Ремонт замка", "от 20 BYN"),
    ("Извлечение обломка ключа", "от 25 BYN"),
    ("Ночной тариф (22:00–7:00)", "+15 BYN"),
]


def generate_llms_txt() -> str:
    lines = [
        "# ЗамокСервис Могилёв",
        "",
        "> Срочное аварийное вскрытие замков в Могилёве и Могилёвской области, Беларусь. "
        "Круглосуточный выезд мастера без повреждения дверей и замков.",
        "",
        "## Контакты",
        f"- Телефон: [{PHONE}](tel:{PHONE_TEL})",
        f"- Telegram: {TELEGRAM_URL}",
        f"- Viber: {VIBER_URL}",
        f"- WhatsApp: {WHATSAPP_URL}",
        f"- Email: {EMAIL}",
        f"- Сайт: {DOMAIN}/",
        "",
        "## Основные услуги",
        f"- [Вскрытие замков — главная]({DOMAIN}/): двери, авто, сейфы от 30 BYN",
        f"- [Вскрытие автомобилей]({DOMAIN}/vskrytie-avto.html): от 40 BYN, все марки",
        f"- [Ремонт замков]({DOMAIN}/remont-zamkov.html): от 20 BYN, выезд мастера",
        f"- [Замена замков]({DOMAIN}/zamena-zamkov.html): от 25 BYN, Cisa, Kale, Гардиан",
        "",
        "## Города обслуживания",
    ]
    for c in CITIES:
        href = DOMAIN + "/" if c["slug"] == "mogilev" else f"{DOMAIN}/{c['file']}"
        lines.append(f"- [{c['name']}]({href}): выезд {c['time']}")
    lines += [
        "",
        "## Блог",
        f"- [Все статьи]({DOMAIN}/blog/)",
    ]
    for p in published_articles():
        lines.append(f"- [{p['title']}]({DOMAIN}/blog/{p['slug']}.html)")
    lines += [
        "",
        "## Optional",
        f"- [Полная информация для AI]({DOMAIN}/llms-full.txt)",
        f"- [Sitemap]({DOMAIN}/sitemap.xml)",
        f"- [Robots.txt]({DOMAIN}/robots.txt)",
    ]
    return "\n".join(lines) + "\n"


def generate_llms_full_txt() -> str:
    lines = [
        "# ЗамокСервис Могилёв — полная информация для AI-поиска",
        "",
        "## О компании",
        "ЗамокСервис — служба срочного вскрытия замков в Могилёве и Могилёвской области (Беларусь).",
        "Работаем с 2010 года, круглосуточно 24/7. Выезд мастера на дом, в офис, к автомобилю.",
        "В 95% случаев вскрываем без повреждения двери и замка. Цена называется до начала работ.",
        "",
        "## Контакты",
        f"- Телефон: {PHONE} ({PHONE_TEL})",
        f"- Telegram: {TELEGRAM_URL}",
        f"- Viber: {VIBER_URL}",
        f"- WhatsApp: {WHATSAPP_URL}",
        f"- Email: {EMAIL}",
        f"- Координаты: 53.8945, 30.3307 (Могилёв)",
        "",
        "## Прайс-лист 2026",
    ]
    for name, price in PRICES:
        lines.append(f"- {name}: {price}")
    lines += ["", "## Услуги по категориям"]
    for slug, svc in SERVICE_COMBOS.items():
        lines.append(f"### {svc['h1']} ({svc['price']})")
        lines.append(svc["desc"])
        lines.append(f"Страница: {DOMAIN}/{slug}.html")
        for c in CITIES:
            url = f"{DOMAIN}/uslugi/{slug}-{c['slug']}.html"
            lines.append(f"- {svc['title_short']} в {c['name']} ({c['time']}): {url}")
        lines.append("")
    lines += ["## Города и время выезда"]
    for c in CITIES:
        href = DOMAIN + "/" if c["slug"] == "mogilev" else f"{DOMAIN}/{c['file']}"
        lines.append(f"- **{c['name']}** ({c['time']}): {href}")
        lines.append(f"  {c['local']}")
    lines += ["", "## Частые вопросы (FAQ)"]
    for q, a in FAQ_GLOBAL:
        lines.append(f"**Q: {q}**")
        lines.append(f"A: {a}")
        lines.append("")
    lines += ["## Блог — полезные статьи"]
    for p in published_articles():
        lines.append(f"- [{p['title']}]({DOMAIN}/blog/{p['slug']}.html) ({p['date']}, {p.get('read', '')})")
        lines.append(f"  {p['desc']}")
    lines += [
        "",
        "## Ключевые запросы",
        "вскрытие замков могилёв, замочный мастер могилёв, аварийное вскрытие, "
        "вскрытие дверей, вскрытие авто, открыть машину, замена замков, ремонт замков, "
        "могилёвская область, бобруйск, горки, осиповичи",
    ]
    return "\n".join(lines) + "\n"


def main():
    (ROOT / "llms.txt").write_text(generate_llms_txt(), encoding="utf-8")
    (ROOT / "llms-full.txt").write_text(generate_llms_full_txt(), encoding="utf-8")
    print("Generated llms.txt and llms-full.txt")


if __name__ == "__main__":
    main()
