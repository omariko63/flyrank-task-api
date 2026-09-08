# To-Do List API

This is a small FastAPI project that exposes a simple to-do list API.
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

FastAPI also exposes the interactive Swagger documentation at `http://127.0.0.1:8000/docs` and the OpenAPI schema at `http://127.0.0.1:8000/openapi.json`.

## Database

Tasks are stored in SQLite so the data persists between server restarts. SQLite was chosen because it is lightweight, requires no separate database server, and stores the complete database in a single portable file. It is a good fit for this small local API while still providing SQL queries and transactions.

The database is stored in the project root as `tasks.db`. The application creates the database and `tasks` table automatically when it starts if they do not already exist.

### Database Viewer

The SQLite database was opened in DB Browser for SQLite:

![Tasks database opened in DB Browser for SQLite](database-viewer.png)

### Example SQL Query

The following query was executed against `tasks.db` to list completed tasks:

```sql
SELECT id, title, done
FROM tasks
WHERE done = 1;
```
