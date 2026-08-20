# Рабочая папка

Сюда кладите свои данные (не коммитьте телефоны и адреса в публичный репозиторий без нужды).

```text
input/     — products.yaml / products.csv
output/    — готовый avito_listings.xlsx
images/    — скачанные фото (если --download-images)
seller.yaml — копия examples/seller-config.example.yaml
```

Быстрый старт:

```bash
cp examples/seller-config.example.yaml workspace/seller.yaml
cp examples/products.example.yaml workspace/input/products.yaml
# отредактируйте файлы
python -m avito_agent generate \
  --products workspace/input/products.yaml \
  --config workspace/seller.yaml \
  --output workspace/output/avito_listings.xlsx
```
