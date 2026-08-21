# AGENTS.md

## Dissertation writer

При задачах про диссертацию, главы, введение, заключение, литературу, импорт DOCX или академическое редактирование:

1. Следуй skill `dissertation-agent/.cursor/skills/dissertation-writer/SKILL.md`
2. Читай конфиг `dissertation-agent/workspace/project.yaml` (или example)
3. Для `.docx` используй `dissertation-agent/tools/import_docx.py` и складывай результат в `workspace/drafts/`
4. Работай по разделам, не выдумывай источники и данные
5. Отвечай на языке пользователя (по умолчанию русский)
