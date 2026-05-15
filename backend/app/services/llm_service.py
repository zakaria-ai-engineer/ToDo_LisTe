"""
llm_service.py — Google Gemini AI inference service.
"""
import logging
import json

from google import genai
from google.genai import types
from fastapi import HTTPException
from app.config.settings import settings
from app.utils.validators import validate_priority

log = logging.getLogger(__name__)

_client: genai.Client | None = None

SYSTEM_PROMPT = """You are a To-Do assistant. Return ONLY a JSON object. No extra talk.
- To ADD a task: {"action": "create", "title": "extracted task name", "priority": "Medium"}
- To DELETE a task: {"action": "delete", "title": "extracted task name"}
- To UPDATE a task: {"action": "update", "title": "extracted task name"}
- If it is a greeting or casual chat, return: {"action": "chat", "message": "your natural friendly reply in Darija/Arabic"}"""

def get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client

def _normalize(parsed: dict) -> dict:
    action = parsed.get("action", "")
    
    if action in ("create", "add_task", "create_task", "add"):
        parsed["action"] = "add_task"
        data = parsed.get("data", {})
        possible_title = data.get("title", parsed.get("title", parsed.get("task", parsed.get("name", parsed.get("task_name", "")))))
        parsed["title"] = possible_title
        parsed["priority"] = data.get("priority", parsed.get("priority", "medium"))
    elif action in ("delete", "delete_task", "remove", "remove_task"):
        parsed["action"] = "delete_task"
        parsed["target"] = parsed.get("id", parsed.get("title", parsed.get("target", "")))
    elif action in ("update", "update_task", "edit", "edit_task"):
        parsed["action"] = "update_task"
        parsed["target"] = parsed.get("id", parsed.get("title", parsed.get("target", "")))
        parsed["new_data"] = parsed.get("data", parsed.get("new_data", parsed))
    elif action in ("show", "show_tasks", "list", "list_tasks", "get_tasks"):
        parsed["action"] = "show_tasks"
    elif action in ("clear", "clear_tasks", "delete_all"):
        parsed["action"] = "clear_tasks"

    if parsed.get("action") == "add_task":
        parsed["priority"] = validate_priority(parsed.get("priority"))
        
    parsed.setdefault("bot_reply", "")
    if "message" in parsed and not parsed.get("bot_reply"):
        parsed["bot_reply"] = parsed.get("message")
        
    parsed.setdefault("title",    None)
    parsed.setdefault("target",   None)
    parsed.setdefault("new_data", None)
    parsed.setdefault("deadline", None)
    return parsed

async def parse_user_intent(message: str) -> list[dict]:
    if not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY not set in .env"
        )

    client = get_client()
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {message}"

    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                temperature=settings.LLM_TEMPERATURE,
                max_output_tokens=1024,
            ),
        )
        raw = response.text.strip()
        log.info("Gemini raw output:\n%s", raw)

        cleaned = raw.replace("```json", "").replace("```", "").strip()
        
        if cleaned.startswith("{") or cleaned.startswith("["):
            try:
                parsed_data = json.loads(cleaned)
                if isinstance(parsed_data, dict):
                    actions = [parsed_data]
                elif isinstance(parsed_data, list):
                    actions = parsed_data
                else:
                    actions = [{"action": "chat", "message": "عذراً زكرياء، وقع مشكل بسيط. حاول عاوتاني."}]
            except json.JSONDecodeError as e:
                actions = [{"action": "chat", "message": "عذراً زكرياء، وقع مشكل بسيط. حاول عاوتاني."}]
        else:
            actions = [{"action": "chat", "message": raw}]

    except Exception as e:
        log.error("Gemini API error: %s", e)
        actions = [{"action": "chat", "message": "عذراً زكرياء، وقع مشكل بسيط. حاول عاوتاني."}]

    return [_normalize(a) for a in actions]
