# Repository Guidelines

## Project Structure & Module Organization

This is an asynchronous FastAPI todo API. Application code lives in `app/`:

- `app/main.py` creates the application, registers routes, and handles HTTP errors.
- `app/api/` contains thin route handlers (currently `todo.py`).
- `app/services/` contains database-backed business logic.
- `app/schemas/` defines Pydantic request, response, pagination, and sorting models.
- `app/database/` contains the async SQLAlchemy engine, base class, and ORM models in `models/`.
- `alembic/versions/` holds generated database migrations; `alembic/env.py` configures Alembic.

Keep new features aligned with this flow: schema, model, service, route, then migration where persistence changes. Add tests under `tests/` when introducing test coverage.

## Build, Test, and Development Commands

Use the checked-in `uv.lock` to keep dependencies reproducible:

```bash
uv sync --dev             # create/update the local environment
uv run poe dev            # run FastAPI development server
uv run poe db-migrate     # apply Alembic migrations
uv run poe db-generate -m "add tags"  # generate a migration after model changes
```

The service reads `database_url` from `.env`; set it to a valid async database URL before running migrations or the server. FastAPI exposes interactive API documentation at `/docs` while the server is running. No automated test command is currently configured.

## Coding Style & Naming Conventions

Follow the existing Python style: four-space indentation, snake_case for modules, functions, fields, and variables; PascalCase for classes; and descriptive async names such as `get_all_todos`. Keep imports grouped (standard library, third-party, local) and add type annotations to public functions. Define request/response validation in Pydantic schemas rather than route handlers. Route handlers should delegate SQLAlchemy work to services and obtain `AsyncSession` through `get_db`.

## Testing Guidelines

There is no committed test suite or coverage threshold. For new behavior, add focused `pytest` tests in `tests/` using names such as `test_create_todo_returns_created_record`. Cover successful responses, validation errors, and missing-resource cases; isolate database tests with a test database and applied migrations. Document any new test dependency and add the test command to `pyproject.toml`.

## Commit & Pull Request Guidelines

Recent commits use Conventional Commit-style subjects, for example `feat(todos): added the listing API`. Use concise imperative subjects such as `fix(todo): handle empty health table`. Keep migrations with the model change that requires them. Pull requests should explain the API or schema change, list migration/configuration steps, link the relevant issue when available, and include request/response examples or `/docs` screenshots for endpoint changes.
