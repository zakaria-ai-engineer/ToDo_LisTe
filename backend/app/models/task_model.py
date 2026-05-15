"""
task_model.py — MongoDB document factory for tasks.
"""
from datetime import datetime, timezone


def new_task_doc(title: str, priority: str, deadline: str | None, user_id: str) -> dict:
    return {
        "title":      title.strip(),
        "priority":   priority,
        "deadline":   deadline,
        "done":       False,
        "user_id":    user_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
