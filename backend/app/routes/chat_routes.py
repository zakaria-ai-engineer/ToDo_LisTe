"""
chat_routes.py — POST /chat (JWT protected).
Gemini interprets the message → backend executes MongoDB action.
"""
from fastapi import APIRouter, Depends
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.llm_service import parse_user_intent
from app.services.task_service import (
    create_task, delete_tasks_by_title, delete_completed_tasks,
    update_tasks_by_title, clear_all_tasks, get_all_tasks, find_tasks_by_title
)
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest, user: dict = Depends(get_current_user)):
    uid    = user["user_id"]
    actions = await parse_user_intent(req.message)

    final_reply = ""
    last_action = "unknown"

    for parsed in actions:
        action    = parsed.get("action")
        title     = parsed.get("title")
        priority  = parsed.get("priority", "medium")
        target    = parsed.get("target")
        new_data  = parsed.get("new_data")
        bot_reply = parsed.get("bot_reply", "")

        if action == "add_task" and title:
            create_task(title, priority, parsed.get("deadline"), uid)

        elif action == "delete_task" and target:
            matched = find_tasks_by_title(target, uid)
            if len(matched) > 1:
                bot_reply = "لقيت بزاف ديال المهام بهاد السمية. أي وحدة فيهم بغيتي؟"
            elif len(matched) == 1:
                delete_tasks_by_title(target, uid)
            else:
                bot_reply = "مالقيتش هاد المهمة."

        elif action == "delete_completed_tasks":
            delete_completed_tasks(uid)

        elif action == "update_task" and target and new_data:
            matched = find_tasks_by_title(target, uid)
            if len(matched) > 1:
                bot_reply = "لقيت بزاف ديال المهام بهاد السمية. أي وحدة فيهم بغيتي؟"
            elif len(matched) == 1:
                fields: dict = {}
                if "title" in new_data: fields["title"] = new_data["title"]
                if "priority" in new_data and new_data["priority"] in ("low","medium","high"): 
                    fields["priority"] = new_data["priority"]
                if "deadline" in new_data: fields["deadline"] = new_data["deadline"]
                if "done" in new_data: fields["done"] = bool(new_data["done"])
                
                if fields:
                    update_tasks_by_title(target, fields, uid)
            else:
                bot_reply = "مالقيتش هاد المهمة."

        elif action == "clear_tasks":
            clear_all_tasks(uid)

        elif action == "show_tasks":
            tasks = get_all_tasks(uid)
            if not tasks:
                bot_reply = "Vous n'avez aucune tâche pour le moment."
            else:
                lines = []
                for t in tasks:
                    status = "✅" if t.get("done") else "⏳"
                    pri = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(t.get("priority"), "⚪")
                    lines.append(f"{status} {pri} {t.get('title')}")
                bot_reply = "Voici vos tâches :\n\n" + "\n".join(lines)
            
        elif action == "chat":
            pass # just a conversation
            
        else:
            if not final_reply and len(actions) == 1:
                final_reply = "Sorry, I didn't understand that. Try: 'Add task', 'Delete task', or 'Show tasks'."

        if bot_reply:
            final_reply = bot_reply
            
        if action and action != "unknown":
            last_action = action

    if not final_reply:
        final_reply = "✅ Opération terminée."

    return ChatResponse(bot_reply=final_reply, action=last_action)
