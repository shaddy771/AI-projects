#!/usr/bin/env python3
"""Generate 100 SEO articles with bi-daily schedule from 2026-09-03."""

import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from articles import save_articles  # noqa: E402
from generate_pages import CITIES  # noqa: E402
from shared import BLOG_CONTENT, BLOG_POSTS, PHONE, PHONE_TEL  # noqa: E402

START_DATE = date(2026, 9, 3)
TOTAL_NEW = 100
IMAGES = ["door-unlock", "car-unlock", "lock-repair", "master-work"]

GENERAL_TOPICS = [
    ("umnyj-zamok-dlya-kvartiry", "Умный замок для квартиры: плюсы, минусы и подводные камни",
     "Стоит ли ставить умный замок на входную дверь? Разбираем безопасность, надёжность и стоимость."),
    ("cisa-vs-kale-vs-guardian", "Cisa, Kale или Гардиан: какой замок лучше для входной двери",
     "Сравниваем три популярных бренда замков для квартир в Беларуси."),
    ("zamok-zaklinil-zimoj", "Почему замок заклинивает зимой и как это предотвратить",
     "Мороз, влага и грязь — главные причины заклинивания. Советы от мастера."),
    ("vskrytie-bronirovannoj-dveri", "Вскрытие бронированной двери без повреждений: возможно ли",
     "Как мастера открывают бронированные двери и сколько это стоит в Могилёве."),
    ("elektronnyj-zamok-ne-rabotaet", "Электронный замок не работает: что делать до приезда мастера",
     "Села батарейка, сбился код, не реагирует на карту — пошаговая инструкция."),
    ("kak-zamenit-lichinku-samostoyatelno", "Замена личинки замка своими руками: инструкция и ошибки",
     "Когда можно сменить личинку самому, а когда лучше вызвать мастера."),
    ("vskrytie-sejfa-bez-povrezhdenij", "Вскрытие сейфа без повреждений: методы и цены",
     "Домашние и офисные сейфы — как открыть профессионально."),
    ("skolko-stoit-zamena-zamka-2026", "Сколько стоит замена замка в 2026 году: полный прайс",
     "Актуальные цены на замену личинки, замка и фурнитуры в Могилёвской области."),
    ("nochnoe-vskrytie-zamkov", "Ночное вскрытие замков: тарифы, сроки и безопасность",
     "Что нужно знать при вызове мастера ночью или в праздник."),
    ("vskrytie-garazha", "Вскрытие гаража и навесного замка: методы и стоимость",
     "Как открыть гаражные ворота и навесной замок без поломки."),
    ("zamok-posle-vzloma", "Замок после взлома: ремонт или замена",
     "Что делать после попытки взлома и как восстановить безопасность."),
    ("detskij-zamok-na-dver", "Детский замок на дверь: виды и установка",
     "Защита от детей vs безопасность при пожаре — как выбрать."),
    ("magneticheskij-zamok-dlya-ofisa", "Магнитный замок для офиса: особенности вскрытия",
     "Электромагнитные замки в офисах — как работают и что при сбое."),
    ("vskrytie-mezhkomnatnoj-dveri", "Вскрытие межкомнатной двери: быстро и аккуратно",
     "Заклинило, ключ потерян — как открыть межкомнатную дверь."),
    ("antivzlomnye-nakladki", "Антивзломные накладки на замок: нужны ли они",
     "Защита цилиндра от высверливания и выдавливания — обзор."),
    ("zamok-dlya-dachi", "Какой замок выбрать для дачи и как его вскрыть при потере ключей",
     "Навесные и врезные замки для дачных домов и гаражей."),
    ("vskrytie-avto-zimoj", "Вскрытие автомобиля зимой: особенности и риски",
     "Замёрзший замок, ключи внутри — что делать не усугубляя ситуацию."),
    ("programmirovanie-avto-klyucha", "Программирование автоключа: когда нужен мастер",
     "Чип-ключи, брелоки, Keyless — что делать при потере."),
    ("vskrytie-kommercheskih-pomeshchenij", "Вскрытие коммерческих помещений: документы и порядок",
     "Офис, магазин, склад — что нужно для легального вскрытия."),
    ("zamok-s-dovodchikom", "Замок с доводчиком заклинил: причины и решение",
     "Почему дверь не открывается из-за доводчика и как это исправить."),
    ("vzlomostojkost-zamkov-klass", "Классы взломостойкости замков: что означают цифры",
     "1–4 класс защиты — какой нужен для квартиры и офиса."),
    ("suvaldnyj-vs-cilindrovyj", "Сувальдный или цилиндровый замок: что надёжнее",
     "Сравнение двух типов замков для входной двери."),
    ("vskrytie-metallicheskoj-dveri", "Вскрытие металлической двери: нюансы и цены",
     "Отличия вскрытия металлических и деревянных дверей."),
    ("poteryali-klyuchi-ot-kvartiry", "Потеряли ключи от квартиры: пошаговый план действий",
     "Что делать в первые 30 минут и когда звонить мастеру."),
    ("zamena-zamka-posle-pereezda", "Замена замка после переезда: обязательно ли",
     "Почему смена личинки — must-have при новоселье."),
    ("vskrytie-podvala-i-kladovki", "Вскрытие подвала и кладовки в Могилёве",
     "Заклинило, ключ сломался — как открыть подвальное помещение."),
    ("remont-zamka-posle-remonta-dveri", "Замок не работает после ремонта двери",
     "Типичные ошибки при установке и как их исправить."),
    ("avtomobil-zakrylsya-s-rebenkom", "Автомобиль закрылся с ребёнком внутри: что делать",
     "Экстренное вскрытие авто — приоритетный выезд."),
    ("vskrytie-staroj-derevyannoj-dveri", "Вскрытие старой деревянной двери без повреждений",
     "Особенности работы с деревянными дверями в старом фонде."),
    ("smart-lock-bezopasnost", "Насколько безопасны умные замки с Bluetooth",
     "Уязвимости, риски и рекомендации по настройке."),
    ("zamok-zasuchil-posle-dozhdya", "Замок зас rustел после дождя: как восстановить",
     "Коррозия и влага — профилактика и ремонт."),
    ("vskrytie-ofisnogo-shkafa", "Вскрытие офисного шкафа с замком",
     "Мебельные замки — быстрое открытие без поломки."),
    ("kak-rabotaet-avarijnoe-vskrytie", "Как работает аварийное вскрытие замков: изнутри профессии",
     "Инструменты, методы и этика замочного мастера."),
    ("zamok-ot-kvartiry-v-dveri-soseda", "Открыли не ту дверь: что делать при ошибке с ключом",
     "Путаница с одинаковыми ключами — как избежать."),
    ("vskrytie-avto-bez-klyucha", "Вскрытие авто без ключа: все легальные способы",
     "Методы профессионалов vs опасные «лайфхаки» из интернета."),
    ("zamena-furnitury-dveri", "Замена дверной фурнитуры вместе с замком",
     "Ручки, петли, защёлки — комплексная замена."),
    ("videonablyudenie-i-zamki", "Видеонаблюдение и замки: комплексная безопасность",
     "Как сочетать замки и камеры для защиты дома."),
    ("vskrytie-pri-pozhare", "Вскрытие дверей при пожаре: роль мастера",
     "Экстренный доступ для МЧС и последующий ремонт."),
    ("kodovyy-zamok-ne-otkryvaetsya", "Кодовый замок не открывается: типичные причины",
     "Механические и электронные кодовые замки — диагностика."),
    ("podgotovka-kvartiry-k-otpusku", "Подготовка замков к отъезду в отпуск",
     "Как защитить квартиру и что проверить перед отъездом."),
]

CITY_TOPIC_TEMPLATES = [
    (
        "vskrytie-zamkov-{slug}",
        "Вскрытие замков в {prep}: цены, сроки и советы {year}",
        "Полный гид по аварийному вскрытию замков в {prep}. Выезд {time}, от 30 BYN.",
        "door-unlock",
    ),
    (
        "vskrytie-avto-{slug}",
        "Вскрытие автомобиля в {prep}: что делать при захлопнутых ключах",
        "Как открыть машину в {prep} без повреждений. Все марки, выезд {time}.",
        "car-unlock",
    ),
    (
        "remont-zamkov-{slug}",
        "Ремонт замков в {prep}: когда нужен мастер и сколько стоит",
        "Заклинило, сломался ключ — ремонт замков с выездом в {prep}.",
        "lock-repair",
    ),
    (
        "zamena-zamkov-{slug}",
        "Замена замков в {prep}: выбор, установка и цены {year}",
        "Как выбрать и установить новый замок в {prep}. Cisa, Kale, Гардиан.",
        "lock-repair",
    ),
]


def slugify(text: str) -> str:
    tr = {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
        "ж": "zh", "з": "z", "и": "i", "й": "j", "к": "k", "л": "l", "м": "m",
        "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
        "ф": "f", "х": "h", "ц": "c", "ч": "ch", "ш": "sh", "щ": "sch",
        "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
    }
    s = text.lower()
    out = []
    for ch in s:
        if ch in tr:
            out.append(tr[ch])
        elif ch.isalnum():
            out.append(ch)
        elif ch in " -_":
            out.append("-")
    return re.sub(r"-+", "-", "".join(out)).strip("-")


def build_content(title: str, desc: str, city: dict | None, img: str, topic_type: str) -> str:
    city_block = ""
    city_link = "/"
    if city:
        city_block = f"<p>Мы работаем в {city['prep']} и по всему {city['gen']}. Среднее время выезда — {city['time']}.</p>"
        city_link = "/" if city["slug"] == "mogilev" else f"/{city['file']}"
        city_kw = city["name"]
    else:
        city_kw = "Могилёве и Могилёвской области"

    inline_img = (
        f'<figure class="blog-article__inline-photo">'
        f'<img src="/images/{img}.webp" srcset="/images/{img}-800.webp 800w, /images/{img}.webp 1200w" '
        f'width="640" height="360" alt="{title}" loading="lazy" decoding="async">'
        f'<figcaption>Работа мастера ЗамокСервис — {city_kw}</figcaption></figure>'
    )

    service_links = """
<p>Полезные ссылки: <a href="/">вскрытие замков в Могилёве</a>, 
<a href="/vskrytie-avto.html">вскрытие авто</a>, 
<a href="/remont-zamkov.html">ремонт замков</a>, 
<a href="/zamena-zamkov.html">замена замков</a>.</p>"""

    if city:
        service_links += f"""
<p>Услуги в {city['prep']}: <a href="{city_link}">вскрытие замков</a>, 
<a href="/uslugi/vskrytie-avto-{city['slug']}.html">вскрытие авто</a>.</p>"""

    return f"""
<p>{desc} Эта статья подготовлена мастерами <strong>ЗамокСервис</strong> — службы срочного вскрытия замков в {city_kw}.</p>
<h2>Кратко: главное</h2>
<ul>
<li>Работаем круглосуточно, 7 дней в неделю</li>
<li>Цена называется до начала работ</li>
<li>95% вскрытий — без повреждения двери и замка</li>
<li>Выезд мастера от 15 минут по Могилёву</li>
</ul>
{inline_img}
<h2>Подробности</h2>
<p>{title} — частый запрос жителей {city_kw}. Наши мастера сталкиваются с подобными ситуациями ежедневно и знают, как решить проблему быстро и аккуратно.</p>
<p>Не пытайтесь вскрыть замок самостоятельно отмычками или силой — это повреждает механизм и увеличивает стоимость ремонта. Профессиональное вскрытие стоит от 30 BYN и занимает 10–30 минут.</p>
{city_block}
<h2>Когда вызывать мастера</h2>
<p>Звоните сразу, если: ключ сломался в замке, замок заклинил, потеряли ключи, ключи остались внутри авто или помещения. Чем раньше обратитесь — тем проще и дешевле решение.</p>
{service_links}
<p><a href="tel:{PHONE_TEL}">Позвонить мастеру: {PHONE}</a></p>"""


def build_faq(title: str, city: dict | None) -> list[dict]:
    loc = city["prep"] if city else "Могилёве"
    return [
        {
            "q": f"Сколько стоит {title.lower().split(':')[0]}?",
            "a": f"Стоимость от 30 BYN. Точная цена зависит от типа замка и времени вызова в {loc}. Мастер называет сумму до начала работ.",
        },
        {
            "q": "Можно ли вскрыть без повреждений?",
            "a": "Да, в 95% случаев мы открываем замки профессиональными методами без повреждения двери и механизма.",
        },
        {
            "q": "Как быстро приедет мастер?",
            "a": f"По {loc} — от 15 до 60 минут в зависимости от района. Работаем 24/7.",
        },
    ]


def migrate_legacy() -> list[dict]:
    articles = []
    for p in BLOG_POSTS:
        articles.append({
            "slug": p["slug"],
            "title": p["title"],
            "desc": p["desc"],
            "keywords": f"замки могилёв, {p['slug'].replace('-', ' ')}",
            "date": p["date"],
            "read": p["read"],
            "img": p["img"],
            "status": "published",
            "content": BLOG_CONTENT.get(p["slug"], ""),
            "faq": build_faq(p["title"], None),
            "topic_type": "legacy",
        })
    return articles


def generate_topic_list() -> list[tuple]:
    topics = []
    for slug, title, desc in GENERAL_TOPICS:
        topics.append((slug, title, desc, None, IMAGES[len(topics) % len(IMAGES)], "general"))
    for city in CITIES:
        for tpl_slug, tpl_title, tpl_desc, img in CITY_TOPIC_TEMPLATES:
            if len(topics) >= TOTAL_NEW:
                break
            slug = tpl_slug.format(slug=city["slug"])
            title = tpl_title.format(prep=city["prep"], year="2026", time=city["time"])
            desc = tpl_desc.format(prep=city["prep"], year="2026", time=city["time"])
            topics.append((slug, title, desc, city, img, "city"))
        if len(topics) >= TOTAL_NEW:
            break
    n = 1
    while len(topics) < TOTAL_NEW:
        topics.append((
            f"sovety-po-zamkam-{n}",
            f"Безопасность замков: советы мастера #{n}",
            f"Практические рекомендации по замкам и защите дома — выпуск {n}.",
            None,
            IMAGES[n % len(IMAGES)],
            "general",
        ))
        n += 1
    return topics[:TOTAL_NEW]


def main():
    legacy = migrate_legacy()
    topics = generate_topic_list()
    new_articles = []
    used_slugs = {a["slug"] for a in legacy}

    for i, (slug, title, desc, city, img, topic_type) in enumerate(topics):
        base_slug = slug
        counter = 2
        while slug in used_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1
        used_slugs.add(slug)

        pub_date = START_DATE + timedelta(days=i * 2)
        keywords = title.lower().replace(":", "").replace("—", "")
        if city:
            keywords += f", {city['name'].lower()}, {city['prep'].lower()}"

        article = {
            "slug": slug,
            "title": title,
            "desc": desc,
            "keywords": keywords[:200],
            "date": pub_date.isoformat(),
            "read": f"{5 + (i % 4)} мин",
            "img": img,
            "status": "scheduled",
            "content": build_content(title, desc, city, img, topic_type),
            "faq": build_faq(title, city),
            "topic_type": topic_type,
            "city": city["slug"] if city else None,
        }
        new_articles.append(article)

    all_articles = legacy + new_articles
    save_articles(all_articles)
    print(f"Saved {len(all_articles)} articles ({len(legacy)} legacy + {len(new_articles)} scheduled)")
    print(f"Schedule: {START_DATE} — {new_articles[-1]['date']} (every 2 days)")


if __name__ == "__main__":
    main()
