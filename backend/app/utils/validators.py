"""
validators.py — Input validation utilities.
"""
import re
import json

VALID_PRIORITIES = {"low", "medium", "high"}
VALID_ACTIONS    = {"add_task", "delete_task", "show_tasks", "update_task", "clear_tasks"}

# Default dict returned when JSON parsing fails completely
FALLBACK_RESPONSE: dict = {
    "action":    "chat",
    "title":     None,
    "priority":  "medium",
    "deadline":  None,
    "done":      None,
    "filter":    None,
    "bot_reply": "Désolé, je n'ai pas bien compris. Pouvez-vous reformuler ?",
}


def validate_priority(p: str | None) -> str:
    """Normalize priority value; falls back to 'medium'."""
    return p if p in VALID_PRIORITIES else "medium"


def _strip_markdown(text: str) -> str:
    """Remove markdown code fences and stray backticks."""
    text = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE)
    text = text.replace("`", "")
    return text.strip()


def _repair_truncated_json(text: str) -> str:
    """
    Attempt to close a truncated JSON object by counting braces.
    If the object is missing closing braces, append them.
    """
    open_count  = text.count("{")
    close_count = text.count("}")
    missing = open_count - close_count
    if missing > 0:
        text = text.rstrip().rstrip(",")   # remove trailing comma before close
        text += "}" * missing
    return text


def extract_json(text: str) -> dict:
    """
    Robustly extract the first JSON object from LLM output.

    Strategy (in order):
      1. Strip markdown fences
      2. Try direct json.loads
      3. Regex-extract the first {...} block, then try again
      4. Auto-repair truncated JSON (balance braces), then try again
      5. Return FALLBACK_RESPONSE — never raise, never crash the app
    """
    # ── 1. Clean markdown ────────────────────────────────────────────────────
    cleaned = _strip_markdown(text)

    # ── 2. Direct parse ──────────────────────────────────────────────────────
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # ── 3. Regex: extract first {...} block ──────────────────────────────────
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        candidate = match.group()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            # ── 4. Repair truncated JSON ─────────────────────────────────────
            repaired = _repair_truncated_json(candidate)
            try:
                return json.loads(repaired)
            except json.JSONDecodeError:
                pass

    # ── 5. Fallback — assume it's raw chat text ─────────────────────────────
    import logging
    logging.getLogger(__name__).warning(
        "extract_json: could not parse LLM output, assuming plain text chat.\n"
        "Raw output (first 400 chars): %s", text[:400]
    )
    fallback = dict(FALLBACK_RESPONSE)
    fallback["bot_reply"] = text.strip() if text.strip() else fallback["bot_reply"]
    return fallback


def extract_json_list(text: str) -> list[dict]:
    """
    Robustly extract JSON from LLM output.
    Returns a LIST of dicts. If the LLM returned a single {...}, wraps it in a list.
    If the LLM returned an array [...], parses it.
    Falls back to [FALLBACK_RESPONSE] on complete failure.
    """
    cleaned = _strip_markdown(text)

    # Attempt 1: Direct JSON parsing (could be list or dict)
    try:
        data = json.loads(cleaned)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return [data]
    except json.JSONDecodeError:
        pass

    # Attempt 2: Regex for Array [...]
    match_array = re.search(r"\[.*\]", cleaned, re.DOTALL)
    if match_array:
        candidate = match_array.group()
        try:
            data = json.loads(candidate)
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            # We could do a repair array here if needed, but array truncation is trickier.
            pass

    # Attempt 3: Regex for Object {...} (Fallback to extract_json logic for a single dict)
    single_dict = extract_json(cleaned)
    return [single_dict]
