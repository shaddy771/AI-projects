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
from articles import (  # noqa: E402
    BLOG_PER_PAGE,
    published_articles,
    paginate_articles,
)
from shared import (  # noqa: E402
    BLOG_CONTENT,
    BLOG_POSTS,
    CITY_EXTRA,
    HEAD_ASSETS,
    SERVICE_COMBOS,
    SERVICE_IMAGES,
    ai_head_meta,
    blog_article_schema,
    city_schema,
    combo_schema,
    feedback_form_section,
    float_cta,
    img_tag,
    service_card_html,
    social_bar,
    TELEGRAM_URL,
    VIBER_URL,
    WHATSAPP_URL,
)


def combo_hero_image(service_slug: str) -> str:
    return {
        "vskrytie-avto": SERVICE_IMAGES["car"],
        "remont-zamkov": SERVICE_IMAGES["repair"],
        "zamena-zamkov": SERVICE_IMAGES["door"],
    }.get(service_slug, SERVICE_IMAGES["master"])


def city_services_html(slug: str, prep: str) -> str:
    cards = [
        service_card_html("Вскрытие дверей", "от 35 BYN", SERVICE_IMAGES["door"], link=f"tel:{PHONE_TEL}"),
        service_card_html(
            f'<a href="/uslugi/vskrytie-avto-{slug}.html">Вскрытие авто</a>',
            "от 40 BYN",
            SERVICE_IMAGES["car"],
        ),
        service_card_html(
            f'<a href="/uslugi/zamena-zamkov-{slug}.html">Замена замков</a>',
            "от 25 BYN",
            SERVICE_IMAGES["replace"],
        ),
        service_card_html(
            f'<a href="/uslugi/remont-zamkov-{slug}.html">Ремонт замков</a>',
            "от 20 BYN",
            SERVICE_IMAGES["repair"],
        ),
    ]
    return "\n          ".join(cards)


def city_faq_data(city: dict) -> list[tuple[str, str]]:
    prep, gen, time = city["prep"], city["gen"], city["time"]
    return [
        (f"Сколько стоит вскрытие замка в {prep}?", f"Стоимость от 30 BYN. Точная цена зависит от типа замка и времени вызова. Мастер называет сумму до начала работ в {prep}."),
        (f"Как быстро приедет мастер в {prep}?", f"Среднее время выезда по {gen} — {time}. Мастера дежурят в области для оперативного прибытия."),
        (f"Работаете ли вы в районах {gen}?", f"Да, выезжаем по всему {gen} и прилегающим населённым пунктам. Закрытые населённые пункты — уточняйте по телефону."),
    ]


def city_faq_html(city: dict) -> str:
    return "\n".join(
        f'          <details class="faq-item"><summary>{q}</summary><p>{a}</p></details>'
        for q, a in city_faq_data(city)
    )


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


def page_shell(title, description, keywords, canonical, breadcrumb, body, schema_json=None, og_image="og-cover.jpg") -> str:
    schema = f'  <script type="application/ld+json">\n  {schema_json}\n  </script>\n' if schema_json else ""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <link rel="canonical" href="{canonical}">
{ai_head_meta(title, description, canonical, og_image)}
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
{feedback_form_section()}
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
    schema = city_schema(city, canonical, city_faq_data(city))

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
            <a href="#feedback" class="btn btn--outline btn--lg">Оставить номер</a>
          </div>
{social_bar()}
        </div>
        <figure class="hero__photo">{img_tag("master-work", f"Мастер ЗамокСервис — выезд в {prep}", 360, 270, "eager")}</figure>
      </div>
    </section>
{city_local_html(city)}
    <section class="section">
      <div class="container">
        <h2>Услуги в {prep}</h2>
        <div class="services-grid">
          {city_services_html(slug, prep)}
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
        <figure class="hero__photo">{img_tag(combo_hero_image(service_slug), f"{svc['h1']} в {prep}", 360, 270, "eager")}</figure>
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

    schema = combo_schema(service_slug, city, canonical)
    hero_img = f"{combo_hero_image(service_slug)}.webp"
    bc = f'<a href="/">Главная</a> → <a href="/{service_slug}.html">{svc["title_short"]}</a> → {name}'
    return page_shell(title, desc, kw, canonical, bc, body, schema, hero_img)


def blog_faq_html(faq: list[dict]) -> str:
    if not faq:
        return ""
    items = "\n".join(
        f'          <details class="faq-item"><summary>{f["q"]}</summary><p>{f["a"]}</p></details>'
        for f in faq
    )
    return f"""
    <section class="blog-article__faq">
      <h2>Частые вопросы</h2>
      <div class="faq-list">{items}
      </div>
    </section>"""


def blog_card_html(p: dict) -> str:
    return (
        f'          <article class="blog-card">'
        f'<a href="/blog/{p["slug"]}.html" class="blog-card__thumb">{img_tag(p["img"], p["title"], 480, 270)}</a>'
        f'<div class="blog-card__body"><time datetime="{p["date"]}">{p["date"]}</time>'
        f'<h2><a href="/blog/{p["slug"]}.html">{p["title"]}</a></h2>'
        f'<p>{p["desc"]}</p><span class="blog-card__read">{p["read"]}</span></div></article>'
    )


def pagination_html(page: int, total_pages: int, base_path: str = "/blog/") -> str:
    if total_pages <= 1:
        return ""
    links = []
    for p in range(1, total_pages + 1):
        href = base_path if p == 1 else f"/blog/page-{p}.html"
        cls = "pagination__link pagination__link--active" if p == page else "pagination__link"
        links.append(f'<a href="{href}" class="{cls}">{p}</a>')
    return f'<nav class="pagination" aria-label="Страницы блога">{"".join(links)}</nav>'


def render_blog_index(page: int = 1) -> str:
    all_posts = published_articles()
    posts, total_pages = paginate_articles(all_posts, page, BLOG_PER_PAGE)
    cards = "\n".join(blog_card_html(p) for p in posts)
    pag = pagination_html(page, total_pages)
    title_suffix = f" — страница {page}" if page > 1 else ""
    canonical = f"{DOMAIN}/blog/" if page == 1 else f"{DOMAIN}/blog/page-{page}.html"
    body = f"""
    <section class="section">
      <div class="container">
        <header class="section__header"><h1>Блог о замках и безопасности{title_suffix}</h1><p>Полезные статьи от мастеров ЗамокСервис</p></header>
        <div class="blog-grid">{cards}
        </div>
        {pag}
      </div>
    </section>"""
    bc = '<a href="/">Главная</a> → Блог' + (f' → Страница {page}' if page > 1 else '')
    return page_shell(
        f"Блог — советы по замкам{title_suffix} | ЗамокСервис",
        "Статьи о замках, вскрытии, ремонте и безопасности в Могилёве и области.",
        "блог замки могилёв",
        canonical,
        bc,
        body,
    )


def render_blog_post(post: dict) -> str:
    content = post.get("content") or BLOG_CONTENT.get(post["slug"], "<p>Статья в подготовке.</p>")
    faq_block = blog_faq_html(post.get("faq", []))
    canonical = f"{DOMAIN}/blog/{post['slug']}.html"
    schema = blog_article_schema(post, canonical)
    keywords = post.get("keywords", "замки могилёв")
    body = f"""
    <article class="section blog-article">
      <div class="container blog-article__inner">
        <figure class="blog-article__cover">{img_tag(post["img"], post["title"], 720, 405, "eager")}</figure>
        <header><time datetime="{post["date"]}">{post["date"]}</time><h1>{post["title"]}</h1><p class="blog-article__lead">{post["desc"]}</p></header>
        <div class="blog-article__content">{content}</div>
        {faq_block}
        <div class="blog-article__cta"><a href="tel:{PHONE_TEL}" class="btn btn--primary">Вызвать мастера: {PHONE}</a></div>
      </div>
    </article>"""
    return page_shell(
        f'{post["title"]} | ЗамокСервис',
        post["desc"],
        keywords,
        canonical,
        f'<a href="/">Главная</a> → <a href="/blog/">Блог</a> → {post["title"][:40]}',
        body,
        schema,
        f"{post['img']}.webp",
    )


def generate_sitemap() -> str:
    urls = [("", "weekly", "1.0"), ("/blog/", "weekly", "0.85"), ("/llms.txt", "monthly", "0.5"), ("/llms-full.txt", "monthly", "0.5")]
    for s in ("vskrytie-avto", "remont-zamkov", "zamena-zamkov"):
        urls.append((f"/{s}.html", "monthly", "0.9"))
    for c in CITIES:
        if c["slug"] != "mogilev":
            urls.append((f"/{c['file']}", "monthly", "0.85"))
        for s in SERVICE_COMBOS:
            urls.append((f"/uslugi/{s}-{c['slug']}.html", "monthly", "0.8"))
    for p in published_articles():
        urls.append((f"/blog/{p['slug']}.html", "monthly", "0.75"))
    all_posts = published_articles()
    _, total_pages = paginate_articles(all_posts, 1, BLOG_PER_PAGE)
    for pg in range(2, total_pages + 1):
        urls.append((f"/blog/page-{pg}.html", "weekly", "0.7"))
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
        img_name = combo_hero_image(slug)
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

    (blog / "index.html").write_text(render_blog_index(1), encoding="utf-8")
    all_posts = published_articles()
    _, total_pages = paginate_articles(all_posts, 1, BLOG_PER_PAGE)
    for pg in range(2, total_pages + 1):
        (blog / f"page-{pg}.html").write_text(render_blog_index(pg), encoding="utf-8")
    for post in published_articles():
        (blog / f"{post['slug']}.html").write_text(render_blog_post(post), encoding="utf-8")
    print(f"Blog: {len(published_articles())} published, {total_pages} pages")

    (ROOT / "sitemap.xml").write_text(generate_sitemap(), encoding="utf-8")
    print("Sitemap updated")

    from ai_seo import main as ai_seo_main
    ai_seo_main()


if __name__ == "__main__":
    main()
