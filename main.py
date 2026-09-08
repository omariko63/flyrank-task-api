from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from fastapi import Response
import sqlite3


app = FastAPI()

class TaskCreate(BaseModel):
    title: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


def init_db():
    conn = sqlite3.connect("tasks.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)

    cursor = conn.execute("SELECT COUNT(*) FROM tasks")

    if cursor.fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Learn FastAPI", False),
                ("Build a CRUD API", False),
                ("Complete FlyRank task", True),
            ]
        )

    conn.commit()
    conn.close()

init_db()

tasks = []

def get_db_connection():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
async def root():
    return {
        "name": "Task API", 
        "version": "1.0", 
        "endpoints": ["/tasks"]
    }

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/tasks", description="returns a list of all tasks")
async def get_tasks():
    conn = get_db_connection()
    rows = conn.execute("SELECT id, title, done FROM tasks").fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


@app.get("/tasks/{id}", description="returns task by ID")
async def get_task_by_id(id: int):
    conn = get_db_connection()
    row = conn.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (id,)
    ).fetchone()
    conn.close()
    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )
    return dict(row)


@app.post("/tasks", status_code=201, description="creates a new task")
async def create_task(task: TaskCreate):
    if task.title is None or not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    new_id = max(t["id"] for t in tasks) + 1

    new_task = {
        "id": new_id,
        "title": task.title,
        "done": False,
    }

    tasks.append(new_task)

    return new_task

@app.put("/tasks/{id}", description="updates task by ID")
async def update_task(id: int, updated_task: TaskUpdate):
    for task in tasks:
        if task["id"] == id:

            if updated_task.title is None and updated_task.done is None:
                return JSONResponse(
                    status_code=400,
                    content={"error": "No fields provided to update"}
                )

            if updated_task.title is not None:
                if not updated_task.title.strip():
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Title cannot be empty"}
                    )

                task["title"] = updated_task.title

            if updated_task.done is not None:
                task["done"] = updated_task.done

            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

@app.delete("/tasks/{id}", status_code=204, description="deletes task by id")
async def delete_task(id: int):
    for index, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(index)
            return Response(status_code=204)

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )