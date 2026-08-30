#!/usr/bin/env python3
"""Shared HTML fragments and extended data for site generator."""

import json
import re

DOMAIN = "https://vskrytie-zamkov-mogilev.by"
EMAIL = "info@vskrytie-zamkov-mogilev.by"
PHONE = "+375 (44) 791-39-41"
PHONE_TEL = "+375447913941"
PHONE_VIBER = "375447913941"
TELEGRAM_URL = "https://t.me/zamokservice_mogilev"
VIBER_URL = f"viber://chat?number={PHONE_VIBER}"
WHATSAPP_URL = f"https://wa.me/{PHONE_VIBER}"

HEAD_ASSETS = """  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/css/fonts.css">
  <link rel="stylesheet" href="/css/style.min.css">"""


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def ai_head_meta(title: str, description: str, canonical: str, og_image: str = "og-cover.jpg") -> str:
    """Meta tags and links for AI search engines and LLM crawlers."""
    img_url = f"{DOMAIN}/images/{og_image}" if not og_image.startswith("http") else og_image
    safe_desc = description.replace('"', "&quot;")
    safe_title = title.replace('"', "&quot;")
    return f"""  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  <meta name="author" content="ЗамокСервис Могилёв">
  <meta name="abstract" content="{safe_desc[:200]}">
  <link rel="alternate" type="text/plain" href="{DOMAIN}/llms.txt" title="LLMs.txt — информация для AI-поиска">
  <link rel="alternate" type="text/plain" href="{DOMAIN}/llms-full.txt" title="Полная информация для AI-поиска">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="ru_BY">
  <meta property="og:title" content="{safe_title[:70]}">
  <meta property="og:description" content="{safe_desc[:200]}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="ЗамокСервис Могилёв">
  <meta property="og:image" content="{img_url}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{safe_title[:70]}">
  <meta name="twitter:description" content="{safe_desc[:200]}">
  <meta name="twitter:image" content="{img_url}">"""


def json_ld_script(data) -> str:
    return f'  <script type="application/ld+json">\n  {json.dumps(data, ensure_ascii=False, indent=2)}\n  </script>'


def img_tag(name: str, alt: str, width: int = 400, height: int = 300, loading: str = "lazy") -> str:
    """Responsive WebP image with srcset."""
    return (
        f'<img src="/images/{name}.webp" '
        f'srcset="/images/{name}-800.webp 800w, /images/{name}.webp 1200w" '
        f'sizes="(max-width: 768px) 100vw, {width}px" '
        f'width="{width}" height="{height}" alt="{alt}" loading="{loading}" decoding="async">'
    )


SERVICE_IMAGES = {
    "door": "door-unlock",
    "car": "car-unlock",
    "repair": "lock-repair",
    "replace": "lock-repair",
    "master": "master-work",
}

MAIN_PAGE_SERVICES = [
    ("Вскрытие входных дверей", "от 35 BYN", "door-unlock",
     "Металлические, бронированные и деревянные двери. Замки Cisa, Kale, Гардиан, Mottura и другие.",
     "tel:{phone}", "Вызвать мастера →"),
    ('<a href="/vskrytie-avto.html">Вскрытие автомобилей</a>', "от 40 BYN", "car-unlock",
     "Открытие авто при захлопнутых ключах внутри. Все марки: Volkswagen, BMW, Mercedes, Lada и др.",
     "/vskrytie-avto.html", "Подробнее →"),
    ("Вскрытие сейфов", "от 60 BYN", "lock-repair",
     "Мебельные, офисные и встроенные сейфы. Вскрытие с возможностью дальнейшего использования.",
     "tel:{phone}", "Вызвать мастера →"),
    ('<a href="/zamena-zamkov.html">Замена замков</a> · <a href="/remont-zamkov.html">Ремонт</a>', "от 25 BYN", "lock-repair",
     "Установка новых замков, замена личинок, ремонт после взлома. Подбор надёжной фурнитуры.",
     "/zamena-zamkov.html", "Подробнее →"),
    ("Вскрытие квартир и офисов", "от 35 BYN", "door-unlock",
     "Аварийное вскрытие при потере ключей, заклинивании замка или поломке механизма.",
     "tel:{phone}", "Вызвать мастера →"),
    ("Гаражи и навесные замки", "от 30 BYN", "door-unlock",
     "Вскрытие гаражных ворот, подвалов, складов и навесных замков без повреждений.",
     "tel:{phone}", "Вызвать мастера →"),
]


def main_services_html() -> str:
    cards = []
    for title, price, img, desc, link, label in MAIN_PAGE_SERVICES:
        href = link.format(phone=PHONE_TEL)
        cards.append(service_card_html(title, price, img, desc, href, label))
    return "\n          ".join(cards)


def faq_schema(questions: list[tuple[str, str]]) -> dict:
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in questions
        ],
    }


def breadcrumb_schema(items: list[tuple[str, str]]) -> dict:
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url}
            for i, (name, url) in enumerate(items)
        ],
    }


def business_node(city_name: str | None = None) -> dict:
    name = f"ЗамокСервис — {city_name}" if city_name else "ЗамокСервис Могилёв"
    return {
        "@type": "Locksmith",
        "@id": f"{DOMAIN}/#business",
        "name": name,
        "alternateName": "Вскрытие замков Могилёв",
        "description": "Срочное аварийное вскрытие замков в Могилёве и Могилёвской области, Беларусь. Круглосуточный выезд мастера.",
        "url": DOMAIN + "/",
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "priceRange": "от 30 BYN",
        "image": f"{DOMAIN}/images/og-cover.jpg",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": city_name or "Могилёв",
            "addressRegion": "Могилёвская область",
            "addressCountry": "BY",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 53.8945, "longitude": 30.3307},
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59",
        },
        "sameAs": [TELEGRAM_URL, WHATSAPP_URL],
    }


def city_schema(city: dict, canonical: str, faq_items: list[tuple[str, str]]) -> str:
    name, prep, time = city["name"], city["prep"], city["time"]
    graph = [
        {**business_node(name), "@id": f"{canonical}#business", "areaServed": name},
        {
            "@type": "WebPage",
            "@id": f"{canonical}#webpage",
            "url": canonical,
            "name": f"Вскрытие замков в {prep}",
            "description": f"Срочное вскрытие замков в {prep}. Выезд {time}, 24/7.",
            "inLanguage": "ru-BY",
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
        },
        faq_schema(faq_items),
        breadcrumb_schema([("Главная", DOMAIN + "/"), (name, canonical)]),
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)


def combo_schema(service_slug: str, city: dict, canonical: str) -> str:
    svc = SERVICE_COMBOS[service_slug]
    name, prep, time = city["name"], city["prep"], city["time"]
    img = {"vskrytie-avto": "car-unlock", "remont-zamkov": "lock-repair", "zamena-zamkov": "door-unlock"}.get(
        service_slug, "master-work"
    )
    graph = [
        {
            "@type": "Service",
            "@id": f"{canonical}#service",
            "name": f"{svc['h1']} в {prep}",
            "description": svc["desc"],
            "provider": business_node(name),
            "areaServed": {"@type": "City", "name": name},
            "image": f"{DOMAIN}/images/{img}.webp",
            "offers": {
                "@type": "Offer",
                "price": svc["price"].replace("от ", "").replace(" BYN", ""),
                "priceCurrency": "BYN",
                "availability": "https://schema.org/InStock",
            },
        },
        {
            "@type": "WebPage",
            "url": canonical,
            "name": f"{svc['h1']} в {prep}",
            "description": f"{svc['desc']} Выезд {time}.",
            "inLanguage": "ru-BY",
        },
        breadcrumb_schema([
            ("Главная", DOMAIN + "/"),
            (svc["title_short"], f"{DOMAIN}/{service_slug}.html"),
            (name, canonical),
        ]),
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)


def blog_article_schema(post: dict, canonical: str) -> str:
    graph = [
        {
            "@type": "Article",
            "@id": f"{canonical}#article",
            "headline": post["title"],
            "description": post.get("desc", ""),
            "datePublished": post["date"],
            "dateModified": post.get("modified", post["date"]),
            "inLanguage": "ru-BY",
            "image": f"{DOMAIN}/images/{post['img']}.webp",
            "author": {"@type": "Organization", "name": "ЗамокСервис Могилёв", "url": DOMAIN + "/"},
            "publisher": {
                "@type": "Organization",
                "name": "ЗамокСервис Могилёв",
                "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/favicon.svg"},
            },
            "mainEntityOfPage": canonical,
            "keywords": post.get("keywords", ""),
        },
        breadcrumb_schema([
            ("Главная", DOMAIN + "/"),
            ("Блог", DOMAIN + "/blog/"),
            (post["title"][:50], canonical),
        ]),
    ]
    faq = post.get("faq")
    if faq:
        graph.append(faq_schema([(f["q"], f["a"]) for f in faq]))
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)


def service_page_schema(slug: str, service: dict, canonical: str, faq_items: list[tuple[str, str]]) -> str:
    img = {"vskrytie-avto": "car-unlock", "remont-zamkov": "lock-repair", "zamena-zamkov": "door-unlock"}.get(
        slug, "master-work"
    )
    graph = [
        {
            "@type": "Service",
            "@id": f"{canonical}#service",
            "name": service["schema_name"],
            "description": service["desc"],
            "provider": business_node(),
            "areaServed": {"@type": "AdministrativeArea", "name": "Могилёвская область"},
            "image": f"{DOMAIN}/images/{img}.webp",
            "offers": {
                "@type": "Offer",
                "price": service["price_from"].split()[0],
                "priceCurrency": "BYN",
            },
        },
        faq_schema(faq_items),
        breadcrumb_schema([("Главная", DOMAIN + "/"), (service["h1"], canonical)]),
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)


def service_card_html(
    title: str,
    price: str,
    img: str = "door-unlock",
    desc: str = "",
    link: str = "",
    link_label: str = "Вызвать →",
) -> str:
    """Service card with thumbnail."""
    thumb = f'<figure class="service-card__thumb">{img_tag(img, strip_html(title), 320, 180)}</figure>'
    body = thumb + f"<h3>{title}</h3>"
    if desc:
        body += f"<p>{desc}</p>"
    body += f'<span class="service-card__price">{price}</span>'
    if link:
        body += f'<a href="{link}" class="service-card__link">{link_label}</a>'
    return f'<article class="service-card service-card--photo">{body}</article>'

SOCIAL_SVG = {
    "telegram": '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.2 6.73c-.17 1.77-.89 6.08-1.26 8.06-.16.86-.47 1.15-.77 1.18-.65.06-1.15-.43-1.78-.84-.99-.65-1.55-1.06-2.51-1.69-.89-.58-.31-.9.19-1.42.13-.14 2.44-2.24 2.48-2.43a.17.17 0 00-.04-.16c-.05-.04-.13-.03-.19-.02-.08.02-1.34.87-3.78 2.51-.36.24-.68.37-.97.36-.32-.01-.93-.18-1.39-.34-.56-.18-1-.28-.96-.59.02-.16.24-.33.67-.5 2.62-1.14 4.36-1.89 5.23-2.27 2.49-1.04 3-1.22 3.34-1.22.07 0 .24.02.35.11.09.07.12.17.13.24-.01.05.01.22 0 .34z"/></svg>',
    "viber": '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2c-2.67 0-5.24.93-7.26 2.62C2.76 6.3 2 8.55 2 11.07c0 3.09 1.25 6.05 3.48 8.24l-1.05 3.84 3.95-1.04c1.77.97 3.76 1.48 5.66 1.48h.01c5.52 0 10-4.48 10-10.03C23.05 6.48 18.57 2 12.04 2zm5.8 13.97c-.18.5-1.05.97-1.45 1.03-.37.06-.85.09-1.37-.09-.32-.11-.73-.26-1.26-.51-2.22-1.06-3.67-3.52-3.78-3.68-.1-.16-.9-1.2-.9-2.29 0-1.09.57-1.62.77-1.84.2-.22.44-.28.59-.28.15 0 .3 0 .43.01.14.01.32-.05.5.38.18.43.61 1.49.66 1.6.06.11.1.24.02.39-.08.15-.12.24-.24.37-.12.13-.25.29-.36.39-.12.12-.25.25-.11.49.15.24.65 1.07 1.4 1.73.96.86 1.77 1.13 2.02 1.26.25.13.4.11.55-.07.15-.18.63-.74.8-1 .17-.25.34-.21.57-.13.23.09 1.47.69 1.72.82.25.13.42.19.48.29.07.11.07.64-.11 1.14z"/></svg>',
    "whatsapp": '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.435 9.884-9.881 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>',
    "phone": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z" stroke="currentColor" stroke-width="2"/></svg>',
}

CITY_EXTRA = {
    "mogilev": {"districts": "Ленинский, Октябрьский, центр, Первый–Пятый микрорайоны, заводской район", "landmarks": "проспект Мира, площадь Звёзд, ул. Первомайская", "review": ("«Вызывал ночью — приехали за 18 минут, вскрыли бронированную дверь аккуратно»", "Андрей К.", "Ленинский район")},
    "bobruisk": {"districts": "Центр, Западный, Восточный, Северный микрорайоны", "landmarks": "ТЦ «Парк Сити», «Евроopt», ул. Минская", "review": ("«Ключи в машине у вокзала — открыли за 10 минут, без царапин»", "Дмитрий В.", "центр Бобруйска")},
    "gorki": {"districts": "центр города, микрорайон, частный сектор", "landmarks": "ул. Советская, район больницы", "review": ("«Замок заклинил на даче — мастер приехал из Могилёва, всё починил»", "Сергей П.", "Горки")},
    "osipovichi": {"districts": "центр, ж/д вокзал, микрорайоны", "landmarks": "привокзальная площадь, ул. Ленина", "review": ("«Быстро приехали к вокзалу, открыли машину перед поездом»", "Елена М.", "Осиповичи")},
    "krichev": {"districts": "центр, частный сектор, промзона", "landmarks": "ул. Ленина, район рынка", "review": ("«Вскрыли гараж без повреждений, цена как договаривались»", "Игорь Л.", "Кричev")},
    "byhov": {"districts": "центр города, окраины, частный сектор", "landmarks": "ул. Коммунистическая, центральная площадь", "review": ("«Потерял ключи — вскрыли квартиру и поставили новую личинку»", "Ольга С.", "Быхов")},
    "kostyukovichi": {"districts": "центр, жилые кварталы", "landmarks": "ул. Молодёжная", "review": ("«Работают аккуратно, рекомендую жителям района»", "Наталья Р.", "Костюковичи")},
    "klimovichi": {"districts": "центр, частный сектор", "landmarks": "ул. Советская", "review": ("«Приехали из области, ждали 50 минут — в пределах обещанного»", "Виктор М.", "Климовичи")},
    "shklov": {"districts": "центр, микрорайон, дачи", "landmarks": "ул. Свердлова, набережная Днепра", "review": ("«Открыли офисную дверь в субботу, спасли рабочий день»", "Алексей Т.", "Шклов")},
    "chausy": {"districts": "центр, частный сектор", "landmarks": "ул. Ленина, район школы", "review": ("«Заменили личинку после вскрытия — всё за один визит»", "Марина К.", "Чаусы")},
    "mstislavl": {"districts": "центр, историческая часть, новостройки", "landmarks": "ул. Ленинская, замковая гора", "review": ("«Вскрыли старую деревянную дверь без щелей и повреждений»", "Пётр Н.", "Мстиславль")},
    "krugloe": {"districts": "центр, частный сектор", "landmarks": "ул. Советская", "review": ("«Оперативно, вежливо, с чеком на руки»", "Анна Д.", "Круглое")},
    "glusk": {"districts": "центр, окраины", "landmarks": "ул. Ленина", "review": ("«Ночной вызов — приехали, вскрыли, дверь как новая»", "Роман Б.", "Глусск")},
    "belynichi": {"districts": "центр, частный сектор", "landmarks": "ул. Комсомольская", "review": ("«Второй раз обращаюсь — всегда честная цена»", "Татьяна В.", "Белыничи")},
    "kirovsk": {"districts": "центр, микрорайон", "landmarks": "ул. Мира", "review": ("«Открыли сейф в офисе — аккуратно и быстро»", "Денис К.", "Кировск")},
}

# Fix typos in CITY_EXTRA with proper unicode in generator

SERVICE_COMBOS = {
    "vskrytie-avto": {
        "title_short": "Вскрытие авто",
        "h1": "Вскрытие автомобилей",
        "desc": "Срочное открытие автомобиля при захлопнутых ключах. Все марки, без повреждений кузова и лакокрасочного покрытия.",
        "price": "от 40 BYN",
        "keywords_tpl": "вскрытие авто {city}, открыть машину {prep}, ключи в машине {city}",
    },
    "remont-zamkov": {
        "title_short": "Ремонт замков",
        "h1": "Ремонт замков",
        "desc": "Ремонт заклинивших и повреждённых замков с выездом на дом. Извлечение обломков ключей, настройка механизма.",
        "price": "от 20 BYN",
        "keywords_tpl": "ремонт замков {city}, починить замок {prep}, замок заклинил {city}",
    },
    "zamena-zamkov": {
        "title_short": "Замена замков",
        "h1": "Замена замков",
        "desc": "Замена и установка замков, личинок и фурнитуры. Подбор Cisa, Kale, Гардиан под вашу дверь.",
        "price": "от 25 BYN",
        "keywords_tpl": "замена замков {city}, установка замка {prep}, заменить личинку {city}",
    },
}

BLOG_POSTS = [
    {"slug": "chto-delat-zaklinil-zamok", "title": "Что делать, если заклинил замок: пошаговая инструкция", "desc": "Замок не поворачивается, ключ не выходит — что делать самостоятельно и когда звать мастера.", "date": "2026-08-15", "read": "5 мин", "img": "lock-repair"},
    {"slug": "kak-vybrat-zamok-dlya-dveri", "title": "Как выбрать замок для входной двери в 2026 году", "desc": "Сравнение цилиндровых и сувальдных замков. Cisa, Kale, Гардиан — что лучше для квартиры.", "date": "2026-08-10", "read": "7 мин", "img": "door-unlock"},
    {"slug": "slomalsya-klyuch-v-zamke", "title": "Сломался ключ в замке — можно ли извлечь самому?", "desc": "Почему ломаются ключи, как не усугубить поломку и когда нужен профессионал.", "date": "2026-08-05", "read": "4 мин", "img": "lock-repair"},
    {"slug": "skolko-stoit-vskrytie-zamka", "title": "Сколько стоит вскрытие замка в Могилёве в 2026", "desc": "Актуальные цены на вскрытие дверей, авто и сейфов. От чего зависит стоимость.", "date": "2026-07-28", "read": "6 мин", "img": "master-work"},
    {"slug": "vskrytie-avto-bez-povrezhdeniy", "title": "Вскрытие автомобиля без повреждений: как это работает", "desc": "Методы открытия авто профессионалами. Почему не стоит ломать стекло.", "date": "2026-07-20", "read": "5 мин", "img": "car-unlock"},
    {"slug": "kak-zamenit-lichinku-zamka", "title": "Как заменить личинку замка своими руками и когда лучше вызвать мастера", "desc": "Пошаговая замена личинки. Инструменты, типичные ошибки, стоимость работ.", "date": "2026-07-12", "read": "8 мин", "img": "lock-repair"},
]

BLOG_CONTENT = {
    "chto-delat-zaklinil-zamok": """
<p>Заклинивший замок — одна из самых частых причин срочного вызова мастера в Могилёве. Разберём, что можно сделать самостоятельно, а когда лучше сразу звонить специалисту.</p>
<h2>1. Не форсируйте ключ</h2>
<p>Если ключ не поворачивается — не прилагайте силу. Сломанный ключ внутри замка усложнит и удорожит вскрытие.</p>
<h2>2. Смазка механизма</h2>
<p>Иногда помогает графитовая смазка в замочную щель. Не используйте WD-40 для морозостойких замков зимой без последующей просушки.</p>
<h2>3. Проверьте дверь</h2>
<p>Дверь могла просесть и перекашивать замок. Попробуйte прижать дверь к раме и повернуть ключ.</p>
<h2>4. Вызовите мастера</h2>
<p>Если замок не открывается 5–10 минут — звоните. Профессиональное вскрытие в Могилёве стоит от 30 BYN и занимает 10–20 минут.</p>
<p><a href="tel:{PHONE_TEL}">Позвонить мастеру: {PHONE}</a></p>""".format(PHONE_TEL=PHONE_TEL, PHONE=PHONE),
    "kak-vybrat-zamok-dlya-dveri": """
<p>Надёжный замок — первая линия защиты квартиры. Рассказываем, на что обратить внимание при выборе.</p>
<h2>Класс безопасности</h2>
<p>Для входной двери выбирайте замки не ниже 4 класса взломостойкости. Cisa, Kale K2, Гардиан 30.11 — проверенные варианты.</p>
<h2>Цилиндровый vs сувальдный</h2>
<p>Цилиндровый удобнее (легко сменить личинку), сувальдный надёжнее против отмычек. Часто ставят два замка разных типов.</p>
<h2>Установка</h2>
<p>Неправильная установка сводит на нет класс замка. Рекомендуем профессиональный монтаж — от 45 BYN.</p>""",
    "slomalsya-klyuch-v-zamke": """
<p>Обломок ключа в замке — частая ситуация. Главное — не пытаться вытащить его пинцетом или суперклеем.</p>
<h2>Причины поломки</h2>
<p>Износ ключа, некачественная личинка, попытка открыть заклинивший замок с force.</p>
<h2>Что делать</h2>
<p>Не вставляйте второй ключ. Вызовите мастера — извлечение обломка от 25 BYN, занимает 10–15 минут.</p>""",
    "skolko-stoit-vskrytie-zamka": """
<p>Актуальный прайс на аварийное вскрытие в Могилёве и области на 2026 год.</p>
<ul>
<li>Вскрытие входной двери (цилиндр) — от 35 BYN</li>
<li>Вскрытие сувальдного замка — от 45 BYN</li>
<li>Вскрытие автомобиля — от 40 BYN</li>
<li>Ночной тариф (22:00–7:00) — +15 BYN</li>
</ul>
<p>Точную цену мастер называет до начала работ.</p>""",
    "vskrytie-avto-bez-povrezhdeniy": """
<p>Ключи внутри — не повод бить стекло. Профессионалы открывают 98% автомобилей без следов.</p>
<h2>Методы</h2>
<p>Специальные клинья, трос для дверей с механическими замками, программирование для части современных авто.</p>
<h2>Что не делать</h2>
<p>Не ломайте стекло — ремонт обойдётся в разы дороже вскрытия. Не используйте подручные предметы — повредите лак.</p>""",
    "kak-zamenit-lichinku-zamka": """
<p>Замена личинки — способ сменить ключи без замены всего замка. Стоимость работ от 25 BYN.</p>
<h2>Когда нужна замена</h2>
<p>Потеряли ключ, переехали в новую квартиру, ключи попали к посторонним.</p>
<h2>Самостоятельно или мастер</h2>
<p>Если есть навыки и правильная отвёртка — можно. Для бронированных дверей и сложных замков лучше вызвать мастера.</p>""",
}


def feedback_form_section() -> str:
    return """  <section class="feedback-form" id="feedback" aria-label="Обратная связь">
    <div class="container">
      <form class="feedback-form__inner form" id="feedback-form" action="#" method="post">
        <p class="feedback-form__hint">Неудобно звонить? Оставьте номер — перезвоним в течение нескольких минут</p>
        <div class="feedback-form__row">
          <input class="feedback-form__input form__input" type="text" name="name" placeholder="Ваше имя" autocomplete="name" aria-label="Ваше имя">
          <input class="feedback-form__input form__input" type="tel" name="phone" placeholder="+375 (__) ___-__-__" required autocomplete="tel" aria-label="Телефон">
          <button type="submit" class="feedback-form__submit btn btn--sm">Перезвоните мне</button>
        </div>
        <p class="feedback-form__privacy">Отправляя форму, вы соглашаетесь с <a href="/#privacy">политикой конфиденциальности</a></p>
      </form>
    </div>
  </section>"""


def float_cta() -> str:
    return f"""  <div class="float-cta" aria-label="Мессенджеры и звонок">
    <a href="{TELEGRAM_URL}" class="float-cta__btn float-cta__tg" aria-label="Telegram" rel="noopener" data-social="telegram">{SOCIAL_SVG["telegram"]}</a>
    <a href="{VIBER_URL}" class="float-cta__btn float-cta__viber" aria-label="Viber" data-social="viber">{SOCIAL_SVG["viber"]}</a>
    <a href="{WHATSAPP_URL}" class="float-cta__btn float-cta__wa" aria-label="WhatsApp" rel="noopener" data-social="whatsapp">{SOCIAL_SVG["whatsapp"]}</a>
    <a href="tel:{PHONE_TEL}" class="float-cta__btn float-cta__call" aria-label="Позвонить" data-social="phone">{SOCIAL_SVG["phone"]}</a>
  </div>
  <div class="mobile-bar"><a href="tel:{PHONE_TEL}" class="mobile-bar__call">Позвонить: {PHONE}</a></div>
  <div class="toast" id="toast" role="alert" hidden><p>Заявка отправлена! Перезвоним в течение нескольких минут.</p></div>
  <script src="/js/main.min.js" defer></script>"""


def social_bar() -> str:
    return f"""        <div class="social-bar">
          <a href="{TELEGRAM_URL}" class="social-bar__link social-bar__link--tg" rel="noopener" aria-label="Telegram">{SOCIAL_SVG["telegram"]} Telegram</a>
          <a href="{VIBER_URL}" class="social-bar__link social-bar__link--viber" aria-label="Viber">{SOCIAL_SVG["viber"]} Viber</a>
          <a href="{WHATSAPP_URL}" class="social-bar__link social-bar__link--wa" rel="noopener" aria-label="WhatsApp">{SOCIAL_SVG["whatsapp"]} WhatsApp</a>
        </div>"""
