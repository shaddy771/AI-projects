# Агент объявлений Авито

Готовит **XLSX для автозагрузки Авито**: заголовки, HTML-описания, поиск картинок и базовые колонки фида.

> Агент **не публикует** объявления сам. Для полноценного размещения нужны кабинет компании, тариф/подписка, актуальный шаблон категории и хостинг фото — см. [checklists/full-placement.md](./checklists/full-placement.md).

## Что умеет

- Читать товары из YAML / JSON / CSV
- Генерировать `Title` и `Description` под формат Авито
- Искать изображения (DuckDuckGo) и опционально скачивать их
- Собирать `.xlsx` с листом инструкции и листом объявлений
- Валидировать вход до генерации
- Дать чеклист того, чего не хватает для публикации

## Быстрый старт

```bash
cd avito-agent
python -m venv .venv
source .venv/bin/activate
pip install -e .

cp examples/seller-config.example.yaml workspace/seller.yaml
cp examples/products.example.yaml workspace/input/products.yaml
# заполните адрес и телефон в workspace/seller.yaml

python -m avito_agent validate \
  --products workspace/input/products.yaml \
  --config workspace/seller.yaml

python -m avito_agent generate \
  --products workspace/input/products.yaml \
  --config workspace/seller.yaml \
  --output workspace/output/avito_listings.xlsx
```

Поиск картинок отдельно:

```bash
python -m avito_agent search-images "Samsung Galaxy A55" --limit 5 --download
```

## Структура

```text
avito-agent/
  src/avito_agent/     # CLI и пайплайн
  examples/            # примеры товаров и конфига
  checklists/          # полное размещение и готовность фида
  prompts/             # готовые режимы для Cursor
  .cursor/skills/      # skill агента
  workspace/           # ваши вход/выход (локально)
```

## Колонки XLSX

Базовый набор (товарные категории):

`Id`, `AvitoId`, `Category`, `GoodsType`, `ProductType`, `Title`, `Description`,
`Price`, `ImageUrls`, `ImageNames`, `VideoURL`, `Address`, `ContactPhone`,
`ManagerName`, `ContactMethod`, `AdType`, `Condition`, `Availability`, `ListingFee`

Дополнительные поля категории добавляйте в `extras` у товара или в `extra_defaults` конфига.
**Источник истины** — шаблон из кабинета: [Правила и шаблоны](https://autoload.avito.ru/format/).

## Что ещё нужно для полноценного размещения

Кратко (подробности в чеклисте):

1. **Профиль компании** + тариф/план и подписка на инструменты (для «Товаров» — расширенная/максимальная).
2. Раздел **Автозагрузка** в кабинете и актуальный **шаблон категории**.
3. **Публичные URL фото** (или zip + `ImageNames`), лимит архива с файлом ≤ 100 МБ.
4. Стабильные **Id**, корректный **Address**, целые **Price**, заполненные обязательные параметры категории.
5. Загрузка файла / URL фида по расписанию, разбор **отчёта автозагрузки** и модерации.
6. Деньги/пакеты на размещение; при необходимости — продвижение (`AdStatus`, `Promo*`).
7. Обработка чатов/звонков; аналитика — через кабинет или [API Авито](https://developers.avito.ru/).

Официально: [Автозагрузка для бизнеса](https://www.avito.ru/business/tools/autoload).

## Работа в Cursor

Skill: `avito-listings` (см. `.cursor/skills/avito-listings/SKILL.md`).

Пример запроса:

```text
Сгенерируй XLSX для Авито из workspace/input/products.yaml,
найди по 3 фото на товар и скажи, чего не хватает для публикации.
```

## Ограничения

- Поиск картинок зависит от сети и выдачи; стоковые URL нужно заменить на свои для б/у и уникальных товаров.
- Состав обязательных полей Авито меняется — всегда сверяйте с шаблоном категории.
- Агент не обходит модерацию и не гарантирует публикацию.
