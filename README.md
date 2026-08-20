# AI-projects

Коллекция AI-агентов и инструментов.

## Проекты

| Проект | Описание |
|---|---|
| [avito-agent](./avito-agent/) | Агент: описания, поиск картинок и XLSX для автозагрузки Авито |

## Avito agent — кратко

1. Скопируй `avito-agent/examples/seller-config.example.yaml` → `avito-agent/workspace/seller.yaml`
2. Подготовь список товаров (YAML/CSV) в `avito-agent/workspace/input/`
3. Установи зависимости и сгенерируй файл:

```bash
cd avito-agent && pip install -e .
python -m avito_agent generate \
  --products workspace/input/products.yaml \
  --config workspace/seller.yaml \
  --output workspace/output/avito_listings.xlsx
```

4. Перед публикацией пройди `avito-agent/checklists/full-placement.md`
