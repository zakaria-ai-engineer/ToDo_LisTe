"""
task_service.py — MongoDB CRUD for tasks (title-based).
"""
import re
from fastapi import HTTPException
from pymongo import DESCENDING
from app.config.database import get_tasks_collection
from app.models.task_model import new_task_doc
from app.schemas.task_schema import TaskUpdate
from app.utils.helpers import serialize_doc, to_object_id


def get_all_tasks(user_id: str, priority: str | None = None, done: bool | None = None) -> list:
    col   = get_tasks_collection()
    query = {"user_id": user_id}
    if priority in ("low", "medium", "high"):
        query["priority"] = priority
    if done is not None:
        query["done"] = done
    return [serialize_doc(t) for t in col.find(query).sort("created_at", DESCENDING)]


def create_task(title: str, priority: str, deadline: str | None, user_id: str) -> dict:
    col    = get_tasks_collection()
    result = col.insert_one(new_task_doc(title, priority, deadline, user_id))
    return serialize_doc(col.find_one({"_id": result.inserted_id}))


def update_task_by_id(task_id: str, data: TaskUpdate, user_id: str) -> dict:
    col = get_tasks_collection()
    oid = to_object_id(task_id)
    if not oid:
        raise HTTPException(status_code=400, detail="Invalid task ID")
    fields = {k: v for k, v in data.model_dump().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = col.update_one({"_id": oid, "user_id": user_id}, {"$set": fields})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return serialize_doc(col.find_one({"_id": oid}))


def delete_task_by_id(task_id: str, user_id: str) -> dict:
    col = get_tasks_collection()
    oid = to_object_id(task_id)
    if not oid:
        raise HTTPException(status_code=400, detail="Invalid task ID")
    result = col.delete_one({"_id": oid, "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted", "id": task_id}


def delete_tasks_by_title(title: str, user_id: str) -> int:
    col = get_tasks_collection()
    return col.delete_many({
        "title":   {"$regex": re.escape(title), "$options": "i"},
        "user_id": user_id,
    }).deleted_count


def find_tasks_by_title(title: str, user_id: str) -> list:
    col = get_tasks_collection()
    return list(col.find({
        "title": {"$regex": re.escape(title), "$options": "i"},
        "user_id": user_id
    }))


def update_tasks_by_title(title: str, fields: dict, user_id: str) -> int:
    col = get_tasks_collection()
    return col.update_many(
        {"title": {"$regex": re.escape(title), "$options": "i"}, "user_id": user_id},
        {"$set": fields},
    ).modified_count


def clear_all_tasks(user_id: str) -> int:
    return get_tasks_collection().delete_many({"user_id": user_id}).deleted_count


def delete_completed_tasks(user_id: str) -> int:
    return get_tasks_collection().delete_many({"user_id": user_id, "done": True}).deleted_count
