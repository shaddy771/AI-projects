#!/usr/bin/env python3
"""Extended site builder: combo pages, blog, enriched cities, sitemap."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from generate_pages import (  # noqa: E402
    CITIES,
    DOMAIN,
    PHONE,
    PHONE_TEL,
    areas_grid,
    footer_block,
    header_nav,
    mobile_nav,
    render_services,
)
from shared import (  # noqa: E402
    BLOG_CONTENT,
    BLOG_POSTS,
    CITY_EXTRA,
    HEAD_ASSETS,
    SERVICE_COMBOS,
    float_cta,
    img_tag,
    social_bar,
    TELEGRAM_URL,
    VIBER_URL,
    WHATSAPP_URL,
)


def city_faq_html(city: dict) -> str:
    prep, gen, name, time = city["prep"], city["gen"], city["name"], city["time"]
    items = [
        (f"Сколько стоит вскрытие замка в {prep}?", f"Стоимость от 30 BYN. Точная цена зависит от типа замка и времени вызова. Мастер называет сумму до начала работ в {prep}."),
        (f"Как быстро приедет мастер в {prep}?", f"Среднее время выезда по {gen} — {time}. Мастера дежурят в области для оперативного прибытия."),
        (f"Работаете ли вы в районах {gen}?", f"Да, выезжаем по всему {gen} и прилегающим населённым пунктам. Закрытые населённые пункты — уточняйте по телефону."),
    ]
    return "\n".join(f'          <details class="faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in items)


def city_review_html(city: dict) -> str:
    extra = CITY_EXTRA.get(city["slug"], {})
    default = (f"«Быстро и аккуратно, рекомендую»", "Клиент", city["name"])
    text, author, place = extra.get("review", default)
    return f"""        <blockquote class="review-card review-card--solo">
          <div class="review-card__stars" aria-label="5 из 5">★★★★★</div>
          <p>{text}</p>
          <footer><cite>{author}</cite><span>{place}</span></footer>
        </blockquote>"""


def city_local_html(city: dict) -> str:
    extra = CITY_EXTRA.get(city["slug"], {})
    districts = extra.get("districts", "все районы города")
    landmarks = extra.get("landmarks", "центр города")
    prep = city["prep"]
    return f"""    <section class="section section--alt">
      <div class="container local-info">
        <div class="local-info__text">
          <h2>Районы обслуживания в {prep}</h2>
          <p>Выезжаем во все части города: <strong>{districts}</strong>.</p>
          <p>Частые вызовы рядом с: {landmarks}.</p>
          <p>{city["local"]}</p>
          <div class="local-info__links">
            <a href="/uslugi/vskrytie-avto-{city["slug"]}.html">Вскрытие авто в {prep}</a> ·
            <a href="/uslugi/remont-zamkov-{city["slug"]}.html">Ремонт замков</a> ·
            <a href="/uslugi/zamena-zamkov-{city["slug"]}.html">Замена замков</a>
          </div>
        </div>
        <figure class="local-info__photo">
          {img_tag("door-unlock", f"Вскрытие замков в {prep} без повреждений", 400, 300)}
        </figure>
      </div>
    </section>"""


def page_shell(title, description, keywords, canonical, breadcrumb, body, schema_json=None) -> str:
    schema = f'  <script type="application/ld+json">\n  {schema_json}\n  </script>\n' if schema_json else ""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canonical}">
{HEAD_ASSETS}
{schema}
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
        <li><a href="/blog/">Блог</a></li>
    </ul></nav>
  </header>
  <main>
    <nav class="breadcrumb container" aria-label="Хлебные крошки">{breadcrumb}</nav>
{body}
  </main>
{footer_block()}
{float_cta()}
</body>
</html>"""


def render_city_enriched(city: dict) -> str:
    slug, name, prep, gen, time = city["slug"], city["name"], city["prep"], city["gen"], city["time"]
    canonical = f"{DOMAIN}/" if slug == "mogilev" else f"{DOMAIN}/{city['file']}"
    title = f"Вскрытие замков в {prep} — срочно 24/7 | ЗамокСервис"
    desc = f"Срочное вскрытие замков в {prep}. Выезд {time}, 24/7. Двери, авто, сейфы без повреждений. {PHONE}"
    kw = f"вскрытие замков {name.lower()}, замочный мастер {prep.lower()}"
    schema = f'{{"@context":"https://schema.org","@type":"Locksmith","name":"ЗамокСервис — {name}","telephone":"{PHONE_TEL}","areaServed":"{name}"}}'

    combo_links = "\n".join(
        f'          <a href="/uslugi/{svc}-{slug}.html" class="service-card__link">{SERVICE_COMBOS[svc]["title_short"]} в {prep} →</a>'
        for svc in SERVICE_COMBOS
    )

    body = f"""
    <section class="hero hero--city">
      <div class="hero__bg" aria-hidden="true"></div>
      <div class="container hero__inner">
        <div class="hero__content">
          <div class="hero__badge"><span class="pulse"></span> Выезд в {prep} — {time}</div>
          <h1>Вскрытие замков в <span class="text-accent">{prep}</span></h1>
          <p class="hero__subtitle">Аварийное вскрытие дверей, авто и сейфов в {prep}. Без повреждений, честные цены.</p>
          <div class="hero__cta">
            <a href="tel:{PHONE_TEL}" class="btn btn--primary btn--lg btn--pulse">Позвонить</a>
            <button class="btn btn--outline btn--lg" data-modal="callback">Заказать звонок</button>
          </div>
{social_bar()}
        </div>
      </div>
    </section>
{city_local_html(city)}
    <section class="section">
      <div class="container">
        <h2>Услуги в {prep}</h2>
        <div class="services-grid">
          <article class="service-card"><h3>Вскрытие дверей</h3><p>от 35 BYN</p><a href="tel:{PHONE_TEL}" class="service-card__link">Вызвать →</a></article>
          <article class="service-card"><h3><a href="/uslugi/vskrytie-avto-{slug}.html">Вскрытие авто</a></h3><p>от 40 BYN</p></article>
          <article class="service-card"><h3><a href="/uslugi/zamena-zamkov-{slug}.html">Замена замков</a></h3><p>от 25 BYN</p></article>
          <article class="service-card"><h3><a href="/uslugi/remont-zamkov-{slug}.html">Ремонт замков</a></h3><p>от 20 BYN</p></article>
        </div>
      </div>
    </section>
    <section class="section section--alt">
      <div class="container">
        <h2>Отзыв из {gen}</h2>
{city_review_html(city)}
      </div>
    </section>
    <section class="section" id="faq">
      <div class="container"><h2>Вопросы о вскрытии в {prep}</h2><div class="faq-list">
{city_faq_html(city)}
      </div></div>
    </section>
    <section class="section section--alt">
      <div class="container"><h2>Другие города</h2><div class="areas-grid areas-grid--cities">
{areas_grid(slug)}
      </div></div>
    </section>
    <section class="cta-section"><div class="container cta-section__inner"><div><h2>Вскрытие замков в {prep}</h2></div><a href="tel:{PHONE_TEL}" class="btn btn--white btn--lg">{PHONE}</a></div></section>"""

    bc = f'<a href="/">Главная</a> → {name}'
    return page_shell(title, desc, kw, canonical, bc, body, schema)


def render_combo(service_slug: str, city: dict) -> str:
    svc = SERVICE_COMBOS[service_slug]
    slug, name, prep, gen, time = city["slug"], city["name"], city["prep"], city["gen"], city["time"]
    filename = f"{service_slug}-{slug}.html"
    canonical = f"{DOMAIN}/uslugi/{filename}"
    title = f"{svc['h1']} в {prep} — срочно 24/7 | ЗамокСервис"
    desc = f"{svc['h1']} в {prep} и {gen}. {svc['desc']} Выезд {time}. {PHONE}"
    kw = svc["keywords_tpl"].format(city=name.lower(), prep=prep.lower())
    city_href = "/" if slug == "mogilev" else f"/{city['file']}"

    body = f"""
    <section class="hero hero--city">
      <div class="container hero__inner">
        <div class="hero__content">
          <div class="hero__badge"><span class="pulse"></span> {svc['price']} · выезд {time}</div>
          <h1>{svc['h1']} в <span class="text-accent">{prep}</span></h1>
          <p class="hero__subtitle">{svc['desc']} Работаем в {prep} и по всему {gen}.</p>
          <div class="hero__cta">
            <a href="tel:{PHONE_TEL}" class="btn btn--primary btn--lg btn--pulse">Позвонить: {PHONE}</a>
          </div>
{social_bar()}
        </div>
        <figure class="hero__photo">{img_tag("car-unlock" if service_slug == "vskrytie-avto" else "lock-repair", f"{svc['h1']} в {prep}", 360, 270, "eager")}</figure>
      </div>
    </section>
    <section class="section section--alt">
      <div class="container local-info">
        <div class="local-info__text">
          <h2>{svc['title_short']} по {gen}</h2>
          <p>{city['local']}</p>
          <p>Также смотрите: <a href="{city_href}">вскрытие замков в {prep}</a>, <a href="/{service_slug}.html">{svc['title_short']} по области</a>.</p>
        </div>
      </div>
    </section>
    <section class="cta-section"><div class="container cta-section__inner"><div><h2>{svc['h1']} в {prep}</h2></div><a href="tel:{PHONE_TEL}" class="btn btn--white btn--lg">{PHONE}</a></div></section>"""

    bc = f'<a href="/">Главная</a> → <a href="/{service_slug}.html">{svc["title_short"]}</a> → {name}'
    return page_shell(title, desc, kw, canonical, bc, body)


def render_blog_index() -> str:
    cards = "\n".join(
        f'          <article class="blog-card"><time datetime="{p["date"]}">{p["date"]}</time>'
        f'<h2><a href="/blog/{p["slug"]}.html">{p["title"]}</a></h2>'
        f'<p>{p["desc"]}</p><span class="blog-card__read">{p["read"]}</span></article>'
        for p in BLOG_POSTS
    )
    body = f"""
    <section class="section">
      <div class="container">
        <header class="section__header"><h1>Блог о замках и безопасности</h1><p>Полезные статьи от мастеров ЗамокСервис</p></header>
        <div class="blog-grid">{cards}
        </div>
      </div>
    </section>"""
    return page_shell("Блог — советы по замкам | ЗамокСервис Могилёв", "Статьи о замках, вскрытии, ремонте и безопасности.", "блог замки могилёв", f"{DOMAIN}/blog/", '<a href="/">Главная</a> → Блог', body)


def render_blog_post(post: dict) -> str:
    content = BLOG_CONTENT.get(post["slug"], "<p>Статья в подготовке.</p>")
    body = f"""
    <article class="section blog-article">
      <div class="container blog-article__inner">
        <header><time datetime="{post["date"]}">{post["date"]}</time><h1>{post["title"]}</h1><p class="blog-article__lead">{post["desc"]}</p></header>
        <div class="blog-article__content">{content}</div>
        <div class="blog-article__cta"><a href="tel:{PHONE_TEL}" class="btn btn--primary">Вызвать мастера</a></div>
      </div>
    </article>"""
    return page_shell(post["title"], post["desc"], "замки могилёв", f"{DOMAIN}/blog/{post['slug']}.html", f'<a href="/">Главная</a> → <a href="/blog/">Блог</a> → {post["title"][:40]}', body)


def generate_sitemap() -> str:
    urls = [("", "weekly", "1.0"), ("/blog/", "weekly", "0.85")]
    for s in ("vskrytie-avto", "remont-zamkov", "zamena-zamkov"):
        urls.append((f"/{s}.html", "monthly", "0.9"))
    for c in CITIES:
        if c["slug"] != "mogilev":
            urls.append((f"/{c['file']}", "monthly", "0.85"))
        for s in SERVICE_COMBOS:
            urls.append((f"/uslugi/{s}-{c['slug']}.html", "monthly", "0.8"))
    for p in BLOG_POSTS:
        urls.append((f"/blog/{p['slug']}.html", "monthly", "0.75"))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, freq, pri in urls:
        lines += [f"  <url>", f"    <loc>{DOMAIN}{path}</loc>", f"    <lastmod>2026-08-30</lastmod>", f"    <changefreq>{freq}</changefreq>", f"    <priority>{pri}</priority>", f"  </url>"]
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    uslugi = ROOT / "uslugi"
    uslugi.mkdir(exist_ok=True)
    blog = ROOT / "blog"
    blog.mkdir(exist_ok=True)

    for city in CITIES:
        if city["slug"] == "mogilev":
            continue
        (ROOT / city["file"]).write_text(render_city_enriched(city), encoding="utf-8")
        print(f"City: {city['file']}")

    for svc in SERVICE_COMBOS:
        for city in CITIES:
            fn = f"{svc}-{city['slug']}.html"
            (uslugi / fn).write_text(render_combo(svc, city), encoding="utf-8")
        print(f"Combo: {svc} x {len(CITIES)} cities")

    for slug, html in render_services().items():
        img_name = "car-unlock" if slug == "vskrytie-avto" else "lock-repair"
        photo = f'        <figure class="hero__photo">{img_tag(img_name, SERVICE_COMBOS.get(slug, {}).get("title_short", slug), 360, 270, "eager")}</figure>\n'
        html = html.replace(
            "          </div>\n        </div>\n      </div>\n    </section>\n\n    <section class=\"section\">",
            "          </div>\n" + photo + "        </div>\n      </div>\n    </section>\n\n    <section class=\"section\">",
            1,
        )
        html = html.replace('href="/css/style.css"', 'href="/css/style.min.css"')
        html = html.replace('<link rel="preconnect" href="https://fonts.googleapis.com">', '')
        html = html.replace('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>', '')
        html = re.sub(r'<link href="https://fonts\.googleapis\.com[^>]+>\n?', '', html)
        if '/css/fonts.css' not in html:
            html = html.replace('<link rel="icon"', '<link rel="stylesheet" href="/css/fonts.css">\n  <link rel="stylesheet" href="/css/style.min.css">\n  <link rel="icon"')
        html = html.replace('src="/js/main.js"', 'src="/js/main.min.js"')
        (ROOT / f"{slug}.html").write_text(html, encoding="utf-8")

    (blog / "index.html").write_text(render_blog_index(), encoding="utf-8")
    for post in BLOG_POSTS:
        (blog / f"{post['slug']}.html").write_text(render_blog_post(post), encoding="utf-8")
    print(f"Blog: {len(BLOG_POSTS)} posts")

    (ROOT / "sitemap.xml").write_text(generate_sitemap(), encoding="utf-8")
    print("Sitemap updated")


if __name__ == "__main__":
    main()
