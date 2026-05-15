"""
chat_schema.py — Pydantic schemas for the /chat endpoint.
"""
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    bot_reply: str
    action:    str
