# To-Do List API

This is a small FastAPI project that exposes a simple in-memory to-do list API.
It supports listing tasks, fetching a task by ID, creating a task, updating a task, and deleting a task.

## Install

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Run

Start the API with:

```bash
uvicorn main:app --reload
```

The server will run at `http://127.0.0.1:8000`.

## API Endpoints

| Method | Endpoint | Description | Success Status |
| --- | --- | --- | --- |
| `GET` | `/` | Returns basic API metadata, including the service name, version, and available endpoints. | `200` |
| `GET` | `/health` | Returns a health-check response. | `200` |
| `GET` | `/tasks` | Returns all tasks. | `200` |
| `GET` | `/tasks/{id}` | Returns a task by numeric ID. | `200` |
| `POST` | `/tasks` | Creates a new task with a required non-empty `title`. | `201` |
| `PUT` | `/tasks/{id}` | Updates a task by numeric ID. Supports `title` and `done`. | `200` |
| `DELETE` | `/tasks/{id}` | Deletes a task by numeric ID. | `204` |

## Notes

- Data is stored in memory, so it resets when the server restarts.
- FastAPI also exposes the interactive docs at `/docs` and the OpenAPI schema at `/openapi.json`.

