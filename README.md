# Todo App

A small full-stack todo app: a **Django REST** API backed by **MongoDB**, and a **React** (hooks-only) frontend. Everything runs through Docker Compose.

| Service | Technology | URL |
|---------|------------|-----|
| `app` | React dev server (Node 14) | http://localhost:3000 |
| `api` | Django 3.0 + Django REST Framework (Python 3.8) | http://localhost:8000/todos |
| `mongo` | MongoDB 4.4 | `localhost:27017` |

## Quick start

Prerequisite: [Docker Desktop](https://www.docker.com/products/docker-desktop/).

```sh
git clone https://github.com/1thaju/adbrew_test.git
cd adbrew_test
docker compose up -d
```

- Open http://localhost:3000 to use the app.
- The first start of the `app` container takes a few minutes because it runs `yarn install`. Follow progress with `docker logs -f --tail=50 app`.
- Stop everything with `docker compose down`. Todos are kept in `src/db/`, so they survive restarts.

Use `localhost` (not `127.0.0.1`) in the browser, because Django's `ALLOWED_HOSTS` only lists `localhost`.

## API

Base URL: `http://localhost:8000`. The trailing slash is optional (`/todos` and `/todos/` both work).

### `GET /todos`

Returns all todos, newest first.

```json
[
  {
    "id": "6ac5f27945e32a34e8266e4b",
    "description": "test 2",
    "created_at": "2026-10-07T07:19:21.534000"
  }
]
```

### `POST /todos`

Creates a todo. Request body:

```json
{ "description": "Buy milk" }
```

Returns `201 Created` with the new todo (same shape as above).

The description is trimmed, must be a non-empty string, and may be at most 200 characters.

### Error responses

| Status | When | Body |
|--------|------|------|
| `400 Bad Request` | The payload fails validation (not an object, description missing, not a string, empty, or too long) | `{"error": "Description cannot be empty."}` |
| `503 Service Unavailable` | MongoDB cannot be reached or the operation fails | `{"error": "Todo storage is temporarily unavailable."}` |

Storage failures are logged on the server with the full traceback; only a generic message is sent to the client.

Example:

```sh
curl -i -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"description": "Buy milk"}'
```

## Architecture

### Backend (`src/rest/rest/`)

Requests flow through three layers, and each layer knows only about the one below it:

```
HTTP request -> views.py -> services.py -> repository.py -> MongoDB
```

| File | Responsibility |
|------|----------------|
| `database.py` | Creates the shared `MongoClient` once, from the `MONGO_HOST` and `MONGO_PORT` environment variables. |
| `repository.py` | `TodoRepository`: the only code that reads or writes the `todos` collection. Converts Mongo `_id` to a string `id` and wraps `PyMongoError` in `RepositoryError`. |
| `services.py` | `TodoService`: validates input and applies business rules before calling the repository. |
| `exceptions.py` | `TodoValidationError` and `RepositoryError`, the domain errors the layers use to talk to each other. |
| `views.py` | `TodoListView`: a thin HTTP layer. Calls the service and maps domain errors to status codes. No validation and no database calls. |

Design choices:

- **Separation of concerns.** HTTP, business rules, and persistence can each change without touching the others.
- **Dependency injection.** The service receives its repository in the constructor, so tests use a fake in-memory repository and no database. A different storage backend could be swapped in without changing the service.
- **Domain exceptions.** The view never sees `pymongo` types, so it stays independent of the database.
- **No Django models, serializers or SQLite.** All data is stored through `pymongo` in the `todos` collection of the `test_db` database.

### Frontend (`src/app/src/`)

- `api/todos.js`: `fetchTodos()` and `createTodo()`. The API origin comes from `REACT_APP_API_URL` and defaults to `http://localhost:8000`.
- `useTodos` hook: owns the todo list, loading, error and submitting state. It loads the list on mount and re-fetches after a todo is created.
- `TodoForm` and `TodoList`: presentational components for the form and the list, including loading, empty and error states.

All components are function components using React hooks.

## Docker setup

Both containers use a bind mount of `./src` into `/src`, so code edits are picked up without rebuilding.

- **`api`** is built from the `Dockerfile` (`python:3.8-slim-bullseye`). Dependencies are installed before the source is copied, so editing code does not invalidate the cached dependency layer. It starts Django's `runserver` on `0.0.0.0:8000` (`0.0.0.0` so the port is reachable from outside the container). `MONGO_HOST=mongo` works because Compose services reach each other by service name.
- **`mongo`** uses the official `mongo:4.4` image, bound to all interfaces, with data stored in `./src/db`. A healthcheck pings the server, and `api` uses `depends_on` with `condition: service_healthy` so it starts only once Mongo is ready.
- **`app`** uses `node:14-bullseye` and runs `yarn install && yarn start`. A named volume holds `node_modules` so the bind mount of the source folder does not hide the installed packages. `CHOKIDAR_USEPOLLING` enables hot reload on Windows bind mounts.

### Changes from the starter setup

The original single-image setup no longer built, so it was changed:

- The `python:3.8` base image moved to a newer Debian release without `libssl1.1`, which MongoDB 4.4 requires, and the install failed. The API image is now pinned to a Debian 11 (bullseye) base.
- MongoDB and Node now run from their official images instead of being installed into one large shared image.
- `uWSGI` is removed from the requirements inside the container. It needs a C compiler that the slim image does not have, and it is not used by `runserver`. `pip` is pinned below 24.1 to install the old pinned dependencies.
- Paths in `docker-compose.yml` are relative, so the `ADBREW_CODEBASE_PATH` variable is no longer required.

## Running tests

The backend tests cover the service layer using a fake repository (no database needed):

```sh
docker compose exec -w /src/rest api python manage.py test
```

## Limitations and production notes

This is a development setup, not production-ready:

- It uses Django's `runserver` and the React dev server rather than a production WSGI server and a static build.
- MongoDB has no authentication, and its port is published to the host.
- `GET /todos` returns every todo with no pagination, and `created_at` has no index.
- The provided Django settings were left unchanged: `DEBUG = True`, a hardcoded `SECRET_KEY`, and `CORS_ORIGIN_ALLOW_ALL = True`.
