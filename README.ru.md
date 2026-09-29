# <Название проекта>

[English version](README.md)

Семестровая НИР, начатая с [шаблона лаборатории](https://github.com/Industrial-AI-Research-Lab/nir-project-template). Замените этот абзац описанием проекта: вопрос, данные, ожидаемый результат.

## Быстрый старт

```bash
cp .env.example .env          # заполните ключи; .env не попадает в репозиторий
uv sync                       # ставит пакет и инструменты разработки из uv.lock
uvx pre-commit install        # gitleaks, большие файлы, make check перед каждым коммитом
make check                    # ruff, mypy, pytest
make run                      # один эксперимент: configs/smoke.yaml -> запуск в MLflow
make mlflow                   # интерфейс MLflow над локальной базой mlflow.db
```

Один раз переименуйте пакет: `make rename NAME=<имя_пакета>`, затем `uv lock`.

## Структура

```
src/<пакет>/         код, который импортируется и тестируется: config.py, pipeline.py, __main__.py
tests/               smoke-тест: пайплайн на крошечном входе
configs/             конфиги экспериментов (YAML)
notebooks/           исследовательский анализ; вывод ячеек можно оставить как отчёт о результате
docs/adr/            журнал решений, один файл на решение
docs/meetings/       записи встреч
docs/reading-log.md  журнал чтения статей
data/                не попадает в репозиторий; как получить данные, написано ниже
results/             таблицы и рисунки, экспортированные из кода
.github/             шаблон PR, форма issue для экспериментов, CODEOWNERS, CI
```

## Данные

Где лежат данные и как их получить: <заполните>.

## Эксперименты

Каждый запуск записывается в MLflow (`MLFLOW_TRACKING_URI` в `.env`, по умолчанию локальная база `mlflow.db`). Строка результата: коммит, путь к конфигу, seed, id запуска, метрики.

| коммит | конфиг | seed | id запуска | mse |
|---|---|---|---|---|

## Проверки

`make check` запускается из трёх мест: pre-commit на вашей машине, CI на каждом PR, хук агента. Ветка `<тип>/<короткое-описание>`, заголовок PR `<тип>: ...`; типы: feat, fix, refactor, docs, test, chore, exp.

## LLM-ассистенты

Какими агентами вы пользуетесь и для чего: <заполните>. Инструкции для них: [AGENTS.md](AGENTS.md); общие правила лаборатории подключает `make overlay` ([nir-agent-overlay](https://github.com/Industrial-AI-Research-Lab/nir-agent-overlay)). За код, написанный с агентом, отвечаете вы.

## Памятки

[Практические памятки](https://github.com/Industrial-AI-Research-Lab/project-implementation-manual/blob/master/nir-requirements/recommendations/README.ru.md) из руководства лаборатории: научные статьи, репозиторий и код, трекинг задач, агентные артефакты.

## Лицензия

Шаблон распространяется по MIT. Лицензию своего кода выберите сами и при необходимости замените LICENSE.
