#!/usr/bin/env python3
"""Generate city landing pages for Mogilev region."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://vskrytie-zamkov-mogilev.by"
PHONE = "+375 (29) 123-45-67"
PHONE_TEL = "+375291234567"

CITIES = [
    {"slug": "mogilev", "file": "mogilev.html", "name": "Могилёв", "prep": "Могилёве", "gen": "Могилёва", "time": "15–20 мин", "local": "Выезжаем во все микрорайоны Могилёва: от проспекта Мира до Пятого микрорайона, на заводской район и частный сектор."},
    {"slug": "bobruisk", "file": "bobruisk.html", "name": "Бобруйск", "prep": "Бобруйске", "gen": "Бобруйска", "time": "25–35 мин", "local": "Работаем во всех микрорайонах Бобруйска: Центр, Западный, Восточный, Северный, а также на парковках ТЦ «Парк Сити» и «Евроopt»."},
    {"slug": "gorki", "file": "gorki.html", "name": "Горки", "prep": "Горках", "gen": "Горок", "time": "30–40 мин", "local": "Выезжаем в Горки и населённые пункты Горецкого района."},
    {"slug": "osipovichi", "file": "osipovichi.html", "name": "Осиповичи", "prep": "Осиповичах", "gen": "Осиповичей", "time": "30–45 мин", "local": "Обслуживаем Осиповичи: район ж/д вокзала, центр города, частный сектор и промзона."},
    {"slug": "krichev", "file": "krichev.html", "name": "Кричев", "prep": "Кричеве", "gen": "Кричева", "time": "40–50 мин", "local": "Выезжаем в Кричев и Кричевский район."},
    {"slug": "byhov", "file": "byhov.html", "name": "Быхов", "prep": "Быхове", "gen": "Быхова", "time": "35–45 мин", "local": "Работаем в Быхове и по всему Быховскому району."},
    {"slug": "kostyukovichi", "file": "kostyukovichi.html", "name": "Костюковичи", "prep": "Костюковичах", "gen": "Костюковичей", "time": "45–55 мин", "local": "Обслуживаем Костюковичи и Костюковичский район."},
    {"slug": "klimovichi", "file": "klimovichi.html", "name": "Климовичи", "prep": "Климовичах", "gen": "Климовичей", "time": "50–60 мин", "local": "Выезжаем в Климовичи и по Климовичскому району."},
    {"slug": "shklov", "file": "shklov.html", "name": "Шклов", "prep": "Шклове", "gen": "Шклова", "time": "25–35 мин", "local": "Работаем в Шклове и Шкловском районе."},
    {"slug": "chausy", "file": "chausy.html", "name": "Чаусы", "prep": "Чаусах", "gen": "Чаус", "time": "30–40 мин", "local": "Выезжаем в Чаусы и по Чаусскому району."},
    {"slug": "mstislavl", "file": "mstislavl.html", "name": "Мстиславль", "prep": "Мстиславле", "gen": "Мстиславля", "time": "40–50 мин", "local": "Обслуживаем Мстиславль и Мстиславский район."},
    {"slug": "krugloe", "file": "krugloe.html", "name": "Круглое", "prep": "Круглом", "gen": "Круглого", "time": "30–40 мин", "local": "Выезжаем в Круглое и Круглянский район."},
    {"slug": "glusk", "file": "glusk.html", "name": "Глусск", "prep": "Глусске", "gen": "Глусска", "time": "45–55 мин", "local": "Работаем в Глусске и по Глусскому району."},
    {"slug": "belynichi", "file": "belynichi.html", "name": "Белыничи", "prep": "Белыничах", "gen": "Белыничей", "time": "35–45 мин", "local": "Обслуживаем Белыничи и Белыничский район."},
    {"slug": "kirovsk", "file": "kirovsk.html", "name": "Кировск", "prep": "Кировске", "gen": "Кировска", "time": "40–50 мин", "local": "Выезжаем в Кировск и Кировский район."},
]

def areas_grid(active_slug: str) -> str:
    cards = []
    for c in CITIES:
        href = "/" if c["slug"] == "mogilev" else f"/{c['file']}"
        if c["slug"] == "mogilev":
            href = "/"
        cls = "area-card area-card--active" if c["slug"] == active_slug else "area-card"
        current = ' aria-current="page"' if c["slug"] == active_slug else ""
        cards.append(
            f'          <a href="{href}" class="{cls}"{current}>\n'
            f'            <h3>{c["name"]}</h3>\n'
            f'            <p>{c["time"]}</p>\n'
            f'          </a>'
        )
    return "\n".join(cards)


def header_nav() -> str:
    return """      <nav class="nav" aria-label="Основная навигация">
        <ul class="nav__list">
          <li><a href="/vskrytie-avto.html">Вскрытие авто</a></li>
          <li><a href="/remont-zamkov.html">Ремонт</a></li>
          <li><a href="/zamena-zamkov.html">Замена</a></li>
          <li><a href="/#areas">Города</a></li>
          <li><a href="/#prices">Цены</a></li>
        </ul>
      </nav>"""


def mobile_nav() -> str:
    return """        <li><a href="/vskrytie-avto.html">Вскрытие авто</a></li>
        <li><a href="/remont-zamkov.html">Ремонт замков</a></li>
        <li><a href="/zamena-zamkov.html">Замена замков</a></li>
        <li><a href="/#areas">Города</a></li>
        <li><a href="tel:+375291234567" class="mobile-menu__phone">+375 (29) 123-45-67</a></li>"""


def footer_block() -> str:
    city_links = "\n".join(
        f'          <li><a href="{"/" if c["slug"] == "mogilev" else "/" + c["file"]}">{c["name"]}</a></li>'
        for c in CITIES[:8]
    )
    return f"""  <footer class="footer">
    <div class="container footer__inner">
      <div class="footer__brand">
        <a href="/" class="logo"><span class="logo__text">Замок<span class="logo__accent">Сервис</span></span></a>
        <p>Вскрытие замков в Могилёве и Могилёвской области. Работаем с 2010 года.</p>
      </div>
      <div class="footer__col">
        <h3>Услуги</h3>
        <ul>
          <li><a href="/vskrytie-avto.html">Вскрытие авто</a></li>
          <li><a href="/remont-zamkov.html">Ремонт замков</a></li>
          <li><a href="/zamena-zamkov.html">Замена замков</a></li>
          <li><a href="/#services">Вскрытие дверей</a></li>
        </ul>
      </div>
      <div class="footer__col">
        <h3>Города</h3>
        <ul>
{city_links}
          <li><a href="/#areas">Все города →</a></li>
        </ul>
      </div>
      <div class="footer__col">
        <h3>Контакты</h3>
        <ul>
          <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
          <li><a href="https://wa.me/375291234567" rel="noopener">WhatsApp</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <div class="container"><p>&copy; 2010–2026 ЗамокСервис Могилёв</p></div>
    </div>
  </footer>"""


def float_cta() -> str:
    return f"""  <div class="float-cta" aria-label="Быстрые действия">
    <a href="https://wa.me/375291234567" class="float-cta__btn float-cta__wa" aria-label="WhatsApp" rel="noopener"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.435 9.884-9.881 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg></a>
    <a href="tel:{PHONE_TEL}" class="float-cta__btn float-cta__call" aria-label="Позвонить"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z" stroke="currentColor" stroke-width="2"/></svg></a>
  </div>
  <div class="mobile-bar"><a href="tel:{PHONE_TEL}" class="mobile-bar__call">Позвонить: {PHONE}</a></div>
  <dialog class="modal" id="callback-modal" aria-labelledby="modal-title">
    <div class="modal__content">
      <button class="modal__close" aria-label="Закрыть">&times;</button>
      <h2 id="modal-title">Заказать звонок</h2>
      <form class="form" id="modal-form" action="#" method="post">
        <input class="form__input" type="text" name="name" placeholder="Ваше имя" required>
        <input class="form__input" type="tel" name="phone" placeholder="+375 (__) ___-__-__" required>
        <button type="submit" class="btn btn--primary btn--full">Жду звонка</button>
      </form>
    </div>
  </dialog>
  <div class="toast" id="toast" role="alert" hidden><p>Заявка отправлена!</p></div>
  <script src="/js/main.js" defer></script>"""


def render_city(city: dict) -> str:
    slug = city["slug"]
    name = city["name"]
    prep = city["prep"]
    gen = city["gen"]
    time = city["time"]
    local = city["local"]
    filename = city["file"]
    canonical = f"{DOMAIN}/" if slug == "mogilev" else f"{DOMAIN}/{filename}"
    breadcrumb_href = "/" if slug == "mogilev" else f"/{filename}"

    title = f"Вскрытие замков в {prep} — срочно 24/7, без повреждений | ЗамокСервис"
    description = (
        f"Срочное вскрытие замков в {prep} и {gen}. Выезд за {time}, круглосуточно. "
        f"Вскрытие дверей, авто, сейфов без повреждений. Звоните: {PHONE}"
    )
    keywords = (
        f"вскрытие замков {name.lower()}, вскрытие дверей {prep.lower()}, "
        f"замочный мастер {name.lower()}, аварийное вскрытие {gen.lower()}"
    )

    schema = f"""{{
    "@context": "https://schema.org",
    "@type": "Locksmith",
    "name": "ЗамокСервис — {name}",
    "description": "Срочное вскрытие замков в {prep}",
    "url": "{canonical}",
    "telephone": "{PHONE_TEL}",
    "address": {{
      "@type": "PostalAddress",
      "addressLocality": "{name}",
      "addressRegion": "Могилёвская область",
      "addressCountry": "BY"
    }},
    "areaServed": {{"@type": "City", "name": "{name}"}},
    "openingHoursSpecification": {{
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
      "opens": "00:00",
      "closes": "23:59"
    }},
    "parentOrganization": {{
      "@type": "Locksmith",
      "name": "ЗамокСервис Могилёв",
      "url": "{DOMAIN}/"
    }}
  }}"""

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <meta name="robots" content="index, follow">
  <meta name="geo.region" content="BY-MO">
  <meta name="geo.placename" content="{name}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="Вскрытие замков в {prep} — 24/7">
  <meta property="og:description" content="{description[:160]}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
  <script type="application/ld+json">
  {schema}
  </script>
</head>
<body>
  <header class="header" id="header">
    <div class="container header__inner">
      <a href="/" class="logo" aria-label="ЗамокСервис — на главную">
        <span class="logo__text">Замок<span class="logo__accent">Сервис</span></span>
      </a>
{header_nav()}
      <div class="header__actions">
        <a href="tel:{PHONE_TEL}" class="header__phone"><span>{PHONE}</span></a>
        <button class="btn btn--primary btn--sm header__callback" data-modal="callback">Заказать звонок</button>
        <button class="burger" aria-label="Открыть меню" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span><span></span></button>
      </div>
    </div>
    <nav class="mobile-menu" id="mobile-menu" aria-label="Мобильное меню" hidden>
      <ul>
{mobile_nav()}
      </ul>
    </nav>
  </header>

  <main>
    <section class="hero hero--city">
      <div class="hero__bg" aria-hidden="true"></div>
      <div class="container hero__inner">
        <nav class="breadcrumb" aria-label="Хлебные крошки">
          <a href="/">Главная</a> → {name}
        </nav>
        <div class="hero__content">
          <div class="hero__badge"><span class="pulse"></span> Выезд в {prep} — {time}</div>
          <h1>Вскрытие замков в <span class="text-accent">{prep}</span></h1>
          <p class="hero__subtitle">Срочное аварийное вскрытие дверей, автомобилей и сейфов в {prep} и {gen}. Без повреждений, круглосуточно, честные цены до начала работ.</p>
          <p class="hero__subtitle">{local}</p>
          <div class="hero__cta">
            <a href="tel:{PHONE_TEL}" class="btn btn--primary btn--lg btn--pulse">Позвонить: {PHONE}</a>
            <button class="btn btn--outline btn--lg" data-modal="callback">Заказать звонок</button>
          </div>
          <div class="hero__trust">
            <div class="trust-item"><strong>4.9</strong><span>847 отзывов</span></div>
            <div class="trust-item"><strong>{time.split('–')[0]} мин</strong><span>средний выезд</span></div>
            <div class="trust-item"><strong>24/7</strong><span>без выходных</span></div>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <header class="section__header">
          <h2>Услуги в {prep}</h2>
          <p>Полный спектр замочных работ с выездом на дом или офис.</p>
        </header>
        <div class="services-grid">
          <article class="service-card">
            <h3>Вскрытие входных дверей</h3>
            <p>Металлические, бронированные и деревянные двери в {prep}.</p>
            <span class="service-card__price">от 35 BYN</span>
            <a href="tel:{PHONE_TEL}" class="service-card__link">Вызвать мастера →</a>
          </article>
          <article class="service-card">
            <h3><a href="/vskrytie-avto.html">Вскрытие автомобилей</a></h3>
            <p>Открытие авто при захлопнутых ключах — все марки.</p>
            <span class="service-card__price">от 40 BYN</span>
            <a href="/vskrytie-avto.html" class="service-card__link">Подробнее →</a>
          </article>
          <article class="service-card">
            <h3><a href="/zamena-zamkov.html">Замена замков</a></h3>
            <p>Установка новых замков и личинок после вскрытия.</p>
            <span class="service-card__price">от 25 BYN</span>
            <a href="/zamena-zamkov.html" class="service-card__link">Подробнее →</a>
          </article>
          <article class="service-card">
            <h3><a href="/remont-zamkov.html">Ремонт замков</a></h3>
            <p>Ремонт заклинивших и повреждённых замков.</p>
            <span class="service-card__price">от 20 BYN</span>
            <a href="/remont-zamkov.html" class="service-card__link">Подробнее →</a>
          </article>
          <article class="service-card">
            <h3>Вскрытие сейфов</h3>
            <p>Офисные и домашние сейфы без повреждений.</p>
            <span class="service-card__price">от 60 BYN</span>
            <a href="tel:{PHONE_TEL}" class="service-card__link">Вызвать →</a>
          </article>
          <article class="service-card">
            <h3>Извлечение обломка ключа</h3>
            <p>Аккуратное извлечение сломанного ключа из замка.</p>
            <span class="service-card__price">от 25 BYN</span>
            <a href="tel:{PHONE_TEL}" class="service-card__link">Вызвать →</a>
          </article>
        </div>
      </div>
    </section>

    <section class="section section--alt">
      <div class="container">
        <header class="section__header">
          <h2>Другие города Могилёвской области</h2>
        </header>
        <div class="areas-grid areas-grid--cities">
{areas_grid(slug)}
        </div>
      </div>
    </section>

    <section class="cta-section">
      <div class="container cta-section__inner">
        <div>
          <h2>Нужно вскрыть замок в {prep}?</h2>
          <p>Звоните — мастер выедет за {time.split('–')[0]} минут</p>
        </div>
        <a href="tel:{PHONE_TEL}" class="btn btn--white btn--lg">{PHONE}</a>
      </div>
    </section>
  </main>

{footer_block()}
{float_cta()}
</body>
</html>
"""


def generate_sitemap() -> str:
    urls = [
        ("", "weekly", "1.0"),
        ("/vskrytie-avto.html", "monthly", "0.9"),
        ("/remont-zamkov.html", "monthly", "0.9"),
        ("/zamena-zamkov.html", "monthly", "0.9"),
    ]
    for c in CITIES:
        if c["slug"] == "mogilev":
            continue
        urls.append((f"/{c['file']}", "monthly", "0.85"))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, freq, priority in urls:
        loc = DOMAIN + path
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append("    <lastmod>2026-08-30</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    for city in CITIES:
        if city["slug"] == "mogilev":
            continue  # index.html handled separately
        path = ROOT / city["file"]
        path.write_text(render_city(city), encoding="utf-8")
        print(f"Generated {path.name}")

    for slug, content in render_services().items():
        path = ROOT / f"{slug}.html"
        path.write_text(content, encoding="utf-8")
        print(f"Generated {path.name}")

    sitemap = ROOT / "sitemap.xml"
    sitemap.write_text(generate_sitemap(), encoding="utf-8")
    print("Updated sitemap.xml")


def render_services() -> dict:
    """Return service slug -> HTML content."""
    services = {
        "vskrytie-avto": {
            "title": "Вскрытие автомобилей в Могилёве и области — без повреждений 24/7",
            "h1": "Вскрытие автомобилей",
            "h1accent": "в Могилёве и области",
            "desc": "Срочное вскрытие автомобилей при захлопнутых ключах. Все марки: Volkswagen, BMW, Mercedes, Audi, Lada, Renault. Без повреждений кузова и замков.",
            "keywords": "вскрытие автомобиля могилёв, открыть машину могилёв, вскрытие авто могилёв, ключи в машине могилёв, аварийное вскрытие авто",
            "price_from": "40 BYN",
            "schema_name": "Вскрытие автомобилей",
            "faq": [
                ("Сколько стоит вскрыть автомобиль?", "Стоимость от 40 BYN. Цена зависит от марки, модели и типа замка. Мастер называет точную сумму до начала работ."),
                ("Можно ли открыть машину без царапин?", "Да, мы используем профессиональные методы и инструменты. В 98% случаев автомобиль открывается без повреждений."),
                ("Какие марки авто вы вскрываете?", "Все популярные марки: Volkswagen, BMW, Mercedes, Audi, Toyota, Lada, Renault, Peugeot, Ford и другие."),
            ],
            "items": [
                ("Легковые автомобили", "от 40 BYN", "Открытие при захлопнутых ключах внутри салона"),
                ("Кроссоверы и внедорожники", "от 45 BYN", "Широкий спектр марок и типов замков"),
                ("Коммерческий транспорт", "от 50 BYN", "Фургоны, микроавтобусы, грузовики"),
                ("Извлечение ключа из зажигания", "от 35 BYN", "Если ключ сломался или застрял"),
            ],
        },
        "remont-zamkov": {
            "title": "Ремонт замков в Могилёве и области — с выездом мастера 24/7",
            "h1": "Ремонт замков",
            "h1accent": "в Могилёве и области",
            "desc": "Профессиональный ремонт замков любой сложности: заклинившие механизмы, сломанные ключи, повреждения после взлома. Выезд мастера на дом.",
            "keywords": "ремонт замков могилёв, починить замок могилёв, замок заклинил могилёв, ремонт дверного замка могилёв",
            "price_from": "20 BYN",
            "schema_name": "Ремонт замков",
            "faq": [
                ("Что делать если замок заклинил?", "Не пытайтесь открыть силой — это может сломать механизм. Позвоните нам: мастер диагностирует и отремонтирует замок на месте."),
                ("Можно ли отремонтировать замок после взлома?", "Да, мы восстанавливаем работоспособность замков после взлома или поломки. При необходимости рекомендуем замену."),
                ("Сколько стоит ремонт замка?", "От 20 BYN в зависимости от типа поломки. Точная цена после осмотра."),
            ],
            "items": [
                ("Ремонт цилиндрового замка", "от 20 BYN", "Устранение заклинивания, замена пружин"),
                ("Ремонт сувальдного замка", "от 30 BYN", "Настройка сувальд, замена изношенных деталей"),
                ("Извлечение обломка ключа", "от 25 BYN", "Аккуратное извлечение без повреждения личинки"),
                ("Ремонт после взлома", "от 35 BYN", "Восстановление или замена повреждённых элементов"),
            ],
        },
        "zamena-zamkov": {
            "title": "Замена замков в Могилёве и области — установка с гарантией",
            "h1": "Замена замков",
            "h1accent": "в Могилёве и области",
            "desc": "Замена и установка замков любой сложности: входные двери, межкомнатные, гаражные. Подбор надёжной фурнитуры Cisa, Kale, Гардиан, Mottura.",
            "keywords": "замена замков могилёв, установка замка могилёв, заменить личинку могилёв, замена замка входной двери могилёв",
            "price_from": "25 BYN",
            "schema_name": "Замена замков",
            "faq": [
                ("Сколько стоит замена замка?", "Замена личинки — от 25 BYN, полная замена замка — от 45 BYN плюс стоимость фурнитуры."),
                ("Какой замок лучше установить?", "Рекомендуем Cisa, Kale, Гардиан для входных дверей. Мастер подберёт оптимальный вариант по бюджету и уровню безопасности."),
                ("Можно ли заменить только личинку?", "Да, замена личинки — быстрый и экономичный способ сменить ключи без замены всего замка."),
            ],
            "items": [
                ("Замена личинки замка", "от 25 BYN", "Быстрая смена ключей без замены корпуса"),
                ("Замена замка входной двери", "от 45 BYN", "Установка нового замка + фурнитура"),
                ("Установка дополнительного замка", "от 50 BYN", "Повышение безопасности — второй замок на дверь"),
                ("Замена замка гаража/накладного", "от 30 BYN", "Навесные и врезные замки"),
            ],
        },
    }

    result = {}
    for slug, s in services.items():
        faq_html = "\n".join(
            f'          <details class="faq-item"><summary>{q}</summary><p>{a}</p></details>'
            for q, a in s["faq"]
        )
        items_html = "\n".join(
            f'          <article class="service-card"><h3>{name}</h3><p>{desc}</p>'
            f'<span class="service-card__price">{price}</span>'
            f'<a href="tel:{PHONE_TEL}" class="service-card__link">Вызвать мастера →</a></article>'
            for name, price, desc in s["items"]
        )
        city_links = "\n".join(
            f'          <a href="{"/" if c["slug"] == "mogilev" else "/" + c["file"]}" class="area-card"><h3>{c["name"]}</h3><span>{c["time"]}</span></a>'
            for c in CITIES
        )

        result[slug] = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{s["title"]}</title>
  <meta name="description" content="{s["desc"]} Звоните: {PHONE}">
  <meta name="keywords" content="{s["keywords"]}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{DOMAIN}/{slug}.html">
  <meta property="og:title" content="{s["title"][:70]}">
  <meta property="og:url" content="{DOMAIN}/{slug}.html">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Service",
    "name": "{s["schema_name"]}",
    "description": "{s["desc"]}",
    "provider": {{"@type": "Locksmith", "name": "ЗамокСервис Могилёв", "telephone": "{PHONE_TEL}"}},
    "areaServed": "Могилёвская область",
    "offers": {{"@type": "Offer", "price": "{s["price_from"].split()[0]}", "priceCurrency": "BYN"}}
  }}
  </script>
</head>
<body>
  <header class="header" id="header">
    <div class="container header__inner">
      <a href="/" class="logo"><span class="logo__text">Замок<span class="logo__accent">Сервис</span></span></a>
{header_nav()}
      <div class="header__actions">
        <a href="tel:{PHONE_TEL}" class="header__phone"><span>{PHONE}</span></a>
        <button class="btn btn--primary btn--sm header__callback" data-modal="callback">Заказать звонок</button>
        <button class="burger" aria-label="Меню" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span><span></span></button>
      </div>
    </div>
    <nav class="mobile-menu" id="mobile-menu" hidden><ul>
{mobile_nav()}
    </ul></nav>
  </header>

  <main>
    <section class="hero hero--city">
      <div class="hero__bg" aria-hidden="true"></div>
      <div class="container hero__inner">
        <nav class="breadcrumb"><a href="/">Главная</a> → {s["h1"]}</nav>
        <div class="hero__content">
          <div class="hero__badge"><span class="pulse"></span> Выезд за 15–20 мин · от {s["price_from"]}</div>
          <h1>{s["h1"]} <span class="text-accent">{s["h1accent"]}</span></h1>
          <p class="hero__subtitle">{s["desc"]}</p>
          <div class="hero__cta">
            <a href="tel:{PHONE_TEL}" class="btn btn--primary btn--lg btn--pulse">Позвонить: {PHONE}</a>
            <button class="btn btn--outline btn--lg" data-modal="callback">Бесплатная консультация</button>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <header class="section__header">
          <h2>Виды работ и цены</h2>
          <p>Точная стоимость — после осмотра. Мастер называет цену до начала работ.</p>
        </header>
        <div class="services-grid">
{items_html}
        </div>
      </div>
    </section>

    <section class="section section--dark">
      <div class="container">
        <header class="section__header">
          <h2>Почему ЗамокСервис</h2>
        </header>
        <div class="features-grid">
          <div class="feature"><div class="feature__num">01</div><h3>Опыт 15+ лет</h3><p>Тысячи выполненных работ по всей Могилёвской области.</p></div>
          <div class="feature"><div class="feature__num">02</div><h3>Гарантия</h3><p>Даём гарантию на все виды ремонта и установки.</p></div>
          <div class="feature"><div class="feature__num">03</div><h3>24/7</h3><p>Работаем круглосуточно, включая выходные и праздники.</p></div>
        </div>
      </div>
    </section>

    <section class="section section--alt" id="faq">
      <div class="container">
        <header class="section__header"><h2>Частые вопросы</h2></header>
        <div class="faq-list">
{faq_html}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <header class="section__header"><h2>Работаем по всей области</h2></header>
        <div class="areas-grid areas-grid--cities">
{city_links}
        </div>
      </div>
    </section>

    <section class="cta-section">
      <div class="container cta-section__inner">
        <div><h2>Нужен мастер?</h2><p>Звоните — выедем за 15 минут</p></div>
        <a href="tel:{PHONE_TEL}" class="btn btn--white btn--lg">{PHONE}</a>
      </div>
    </section>
  </main>

{footer_block()}
{float_cta()}
</body>
</html>
"""
    return result


if __name__ == "__main__":
    main()
