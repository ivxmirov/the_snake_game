# Игра Змейка :snake:
Полюбившаяся многим, всемирно известная игра змейка

## Технологии
Основной стек проекта, все зависимости управляются через uv

**Основные:**  
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6+-yellow.svg)](https://www.pygame.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-336791.svg)](https://www.postgresql.org/)

**Инфраструктура:**  
[![uv](https://img.shields.io/badge/uv-0.7+-DE5FE2.svg)](https://docs.astral.sh/uv)
[![Asyncpg](https://img.shields.io/badge/asyncpg-0.31+-2F6790.svg)](https://github.com/MagicStack/asyncpg)
[![Alembic](https://img.shields.io/badge/Alembic-1.18+-6E4B8B.svg)](https://alembic.sqlalchemy.org)

**Качество кода:**  
[![Ruff](https://img.shields.io/badge/Ruff-0.15+-D7FF64.svg)](https://docs.astral.sh/ruff)
[![Mypy](https://img.shields.io/badge/Mypy-1.20+-2F4858.svg)](https://mypy-lang.org)
[![Pytest](https://img.shields.io/badge/Pytest-8.4+-0A9EDC.svg)](https://docs.pytest.org)

## Быстрый старт

1. Клонируйте репозиторий

```bash
git clone https://github.com/ivxmirov/the_snake_game.git
```

2. Настройте переменные окружения

```bash
cp .env.example .env
```
   Отредактируйте файл .env, указав ваш DATABASES_DSN.

3. Установите зависимости (включая dev-зависимости)

```bash
uv sync --group dev
```

4. Примените миграции базы данных

```bash
uv run alembic upgrade head
```

5. Запустите игру
  
```bash
uv run python -m src.main
```

6. Наслаждайтесь игрой !

## Структура

```
the_snake_game
├─ .python-version
├─ alembic
│  ├─ env.py
│  ├─ README
│  ├─ script.py.mako
│  └─ versions
│     ├─ 2755457aa382_fix_defaults.py
│     └─ 9fa6418503a1_add_player_table.py
├─ alembic.ini
├─ pyproject.toml
├─ README.md
├─ setup.cfg
├─ src
│  ├─ database.py
│  ├─ game.py
│  ├─ main.py
│  ├─ models.py
│  ├─ settings.py
│  └─ __init__.py
└─ uv.lock
```

## Автор
ivxmirov - [GitHub](https://github.com/ivxmirov)
