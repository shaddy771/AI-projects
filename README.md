# ЗамокСервис — Вскрытие замков в Могилёве и области

SEO-оптимизированный лендинг для услуг аварийного вскрытия замков.

## Структура сайта

### Главная
- `index.html` — Могилёв (полный лендинг)

### Услуги
- `vskrytie-avto.html` — вскрытие автомобилей
- `remont-zamkov.html` — ремонт замков
- `zamena-zamkov.html` — замена замков

### Города Могилёвской области (15)
| Город | Файл |
|-------|------|
| Могилёв | `index.html` |
| Бобруйск | `bobruisk.html` |
| Горки | `gorki.html` |
| Осиповичи | `osipovichi.html` |
| Кричев | `krichev.html` |
| Быхов | `byhov.html` |
| Костюковичи | `kostyukovichi.html` |
| Климовичи | `klimovichi.html` |
| Шклов | `shklov.html` |
| Чаусы | `chausy.html` |
| Мстиславль | `mstislavl.html` |
| Круглое | `krugloe.html` |
| Глусск | `glusk.html` |
| Белыничи | `belynichi.html` |
| Кировск | `kirovsk.html` |

## Генерация страниц

```bash
python3 scripts/generate_pages.py
```

Перегенерирует все городские страницы, услуги и `sitemap.xml`.

## Запуск локально

```bash
python3 -m http.server 8080
```

## Настройка перед публикацией

1. Замените телефон `+375 (29) 123-45-67` на реальный
2. Обновите домен `vskrytie-zamkov-mogilev.by` в meta-тегах и sitemap
3. Добавьте OG-изображение `images/og-cover.jpg`
4. Подключите Яндекс.Метрику / Google Analytics
