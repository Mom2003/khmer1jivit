from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Nassa Task Management API",
    description="A simple system to manage tasks built with FastAPI",
    version="0.1.0",
)


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(..., min_length=1, max_length=100, description="The title of the task")
    description: str | None = Field(default=None, max_length=500, description="A detailed description of the task")
    status: TaskStatus = Field(default=TaskStatus.TODO, description="Current status of the task")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    status: TaskStatus | None = None


# In-memory database
db: dict[UUID, Task] = {}


@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to the Nassa Task Management API",
        "docs_url": "/docs",
        "status": "operational",
    }


@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
)
def create_task(task_in: TaskCreate):
    task = Task(
        title=task_in.title,
        description=task_in.description,
    )
    db[task.id] = task
    return task


@app.get(
    "/tasks",
    response_model=list[Task],
    tags=["Tasks"],
)
def get_tasks(
    status: TaskStatus | None = Query(default=None, description="Filter tasks by status")
):
    tasks = list(db.values())
    if status:
        tasks = [t for t in tasks if t.status == status]
    # Sort tasks by creation time (newest first)
    tasks.sort(key=lambda t: t.created_at, reverse=True)
    return tasks


@app.get(
    "/tasks/{task_id}",
    response_model=Task,
    tags=["Tasks"],
)
def get_task(task_id: UUID):
    if task_id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return db[task_id]


@app.put(
    "/tasks/{task_id}",
    response_model=Task,
    tags=["Tasks"],
)
def update_task(task_id: UUID, task_in: TaskUpdate):
    if task_id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    task = db[task_id]
    
    update_data = task_in.model_dump(exclude_unset=True)
    if not update_data:
        return task

    # Update fields and standard fields
    for field, value in update_data.items():
        setattr(task, field, value)
    
    task.updated_at = datetime.now(timezone.utc)
    db[task.id] = task
    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
)
def delete_task(task_id: UUID):
    if task_id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    del db[task_id]
    return None
