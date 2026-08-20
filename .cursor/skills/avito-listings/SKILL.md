---
name: avito-listings
description: Готовит объявления Авито: описания, картинки, XLSX для автозагрузки. Использовать при задачах про Авито, автозагрузку, фиды и Excel объявлений.
---

# Агент объявлений Авито

См. полную инструкцию: `avito-agent/.cursor/skills/avito-listings/SKILL.md`.

Кратко:

1. Конфиг продавца → `avito-agent/workspace/seller.yaml`
2. Товары → `avito-agent/workspace/input/` или `examples/`
3. `python -m avito_agent generate --products ... --config ...`
4. Чеклист публикации → `avito-agent/checklists/full-placement.md`
