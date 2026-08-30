# ЗамокСервис — Вскрытие замков в Могилёве и области

## Быстрый старт

```bash
python3 scripts/generate_pages.py   # генерирует все страницы + minify
python3 -m http.server 8080
```

## Масштаб сайта

| Тип | Кол-во |
|-----|--------|
| Главная + города | 15 |
| Услуги (общие) | 3 |
| Услуга × город (`/uslugi/`) | 45 |
| Блог | 6 статей + index |
| **Итого URL в sitemap** | **~70** |

## Структура

- `index.html` — главная (Могилёв)
- `uslugi/` — комбо-страницы (напр. `vskrytie-avto-bobruisk.html`)
- `blog/` — SEO-статьи
- `scripts/generate_pages.py` — полная пересборка
- `css/style.min.css`, `js/main.min.js` — продакшн-ассеты
- `fonts/` — self-hosted Manrope
- `images/` — иллюстрации (замените на фото)

## Мессенджеры

Telegram, Viber, WhatsApp — иконки в hero, float-кнопках и footer.

## Перед публикацией

1. Замените телефон и ссылки мессенджеров
2. Замените SVG в `/images/` на реальные фото (.webp)
3. Подключите Яндекс.Метрику в `js/main.js`
4. Настройте отправку форм (Telegram-бот)
