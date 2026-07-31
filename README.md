# Todo App Server with Python

Use this as a template for starting a python project.

Refer `AGENTS.md` for more info

## Major libraries/tech used -

1. FastAPI - for HTTP server
2. SQL Alchemy - DB ORM
3. Alembic - DB Migrations
4. Pydantic - data validations
5. poethepoet - basic script runner to mimic scripts in package.json in node
6. PostgreSQL - DB

## Things to make sure while using this repo as a template -

1. Use `uv`
2. Verify python version
3. Copy `.env.example` to `.env`
4. Use `uv run poe <script_name>` to run scripts from `pyproject.toml`

## How to start -

```bash
uv sync
```

Add PostgreSQL DB URL in `.env`

If DB models are updated -

```bash
uv run poe db-generate && uv run poe db-migrate
```

Otherwise just the migrate command

```bash
uv run poe db-migrate
```

If everything went alright -

```bash
uv run poe dev
```
