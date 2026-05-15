"""
task_schema.py — Pydantic schemas for task requests and responses.
"""
from typing import Optional
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title:    str  = Field(..., min_length=1, max_length=300)
    priority: str  = Field("medium", pattern="^(low|medium|high)$")
    deadline: Optional[str] = None


class TaskUpdate(BaseModel):
    title:    Optional[str]  = Field(None, min_length=1, max_length=300)
    priority: Optional[str]  = Field(None, pattern="^(low|medium|high)$")
    done:     Optional[bool] = None
    deadline: Optional[str]  = None


class TaskResponse(BaseModel):
    id:         str
    title:      str
    priority:   str
    deadline:   Optional[str]
    done:       bool
    user_id:    str
    created_at: str
