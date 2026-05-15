"""
helpers.py — Shared serialization and utility functions.
"""
from bson import ObjectId


def serialize_doc(doc: dict) -> dict:
    """Convert a MongoDB document to a JSON-safe dict (ObjectId → str)."""
    doc["_id"] = str(doc["_id"])
    return doc


def to_object_id(id_str: str) -> ObjectId:
    """
    Safely convert a string to a MongoDB ObjectId.
    Returns None if the string is not a valid ObjectId.
    """
    try:
        return ObjectId(id_str)
    except Exception:
        return None
