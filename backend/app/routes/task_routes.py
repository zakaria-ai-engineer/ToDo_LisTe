"""
task_routes.py — CRUD endpoints for tasks (all protected by JWT).
"""
from typing import Optional
from fastapi import APIRouter, Depends
from app.schemas.task_schema import TaskCreate, TaskUpdate
from app.services.task_service import (
    get_all_tasks, create_task, update_task_by_id,
    delete_task_by_id, clear_all_tasks,
)
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/")
def list_tasks(
    priority: Optional[str] = None,
    done:     Optional[bool] = None,
    user: dict = Depends(get_current_user),
):
    """Get all tasks for the logged-in user, with optional filters."""
    return get_all_tasks(user["user_id"], priority, done)


@router.post("/", status_code=201)
def create_new_task(
    body: TaskCreate,
    user: dict = Depends(get_current_user),
):
    """Create a new task linked to the logged-in user."""
    task = create_task(
        title    = body.title,
        priority = body.priority,
        deadline = body.deadline,
        user_id  = user["user_id"],
    )
    return {"message": "Task created", "task_id": task["id"]}


@router.put("/{task_id}")
def update_task(
    task_id: str,
    body:    TaskUpdate,
    user:    dict = Depends(get_current_user),
):
    """Update a task by ID (priority, done, title, deadline)."""
    return update_task_by_id(task_id, body, user["user_id"])


@router.delete("/")
def clear_tasks(user: dict = Depends(get_current_user)):
    """Delete ALL tasks belonging to the logged-in user."""
    count = clear_all_tasks(user["user_id"])
    return {"message": "All tasks cleared", "deleted_count": count}


@router.delete("/{task_id}")
def delete_task(
    task_id: str,
    user:    dict = Depends(get_current_user),
):
    """Delete a single task by ID."""
    return delete_task_by_id(task_id, user["user_id"])
