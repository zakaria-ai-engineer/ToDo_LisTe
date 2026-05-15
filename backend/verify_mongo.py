"""
verify_mongo.py — Standalone MongoDB connection & CRUD verification script.

Run from the `backend/` directory:
    python verify_mongo.py

What it does:
  1. Loads MongoDB URI + DB name from backend/.env  (same path logic as settings.py)
  2. Connects with PyMongo (same driver used by the app)
  3. Inserts a timestamped test document into the `tasks` collection
  4. Reads it back to confirm read/write work
  5. Prints a clear success or failure message

Open MongoDB Compass → click Refresh → check the `tasks` collection.
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

# ── 1. Load .env (mirrors settings.py path resolution) ────────────────────────
try:
    from dotenv import load_dotenv
except ImportError:
    print("❌  python-dotenv not installed. Run: pip install python-dotenv")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent          # → backend/
ENV_PATH = BASE_DIR / ".env"

if not ENV_PATH.exists():
    print(f"❌  .env file not found at: {ENV_PATH}")
    sys.exit(1)

load_dotenv(dotenv_path=ENV_PATH, override=True)

import os
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
DB_NAME     = os.getenv("DB_NAME",     "taskbot_db")

print(f"\n{'='*60}")
print(f"  MongoDB Verification Script")
print(f"{'='*60}")
print(f"  URI      : {MONGODB_URL}")
print(f"  Database : {DB_NAME}")
print(f"  .env     : {ENV_PATH}")
print(f"{'='*60}\n")

# ── 2. Connect ─────────────────────────────────────────────────────────────────
try:
    from pymongo import MongoClient
    from pymongo.errors import ServerSelectionTimeoutError
except ImportError:
    print("❌  pymongo not installed. Run: pip install pymongo")
    sys.exit(1)

try:
    client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=3000)
    # Force connection check
    client.admin.command("ping")
    print("  ✅ Step 1/3 — MongoDB server REACHABLE\n")
except ServerSelectionTimeoutError as exc:
    print(f"  ❌ Cannot reach MongoDB at {MONGODB_URL}")
    print(f"     → Is mongod running? Is the URI correct?\n")
    print(f"     Error: {exc}")
    sys.exit(1)

# ── 3. Insert test document (mirrors new_task_doc structure exactly) ───────────
db         = client[DB_NAME]
tasks_col  = db["tasks"]

test_doc = {
    "title":      "Compass Integration Test ✅",
    "priority":   "high",
    "deadline":   None,
    "done":       False,
    "user_id":    "__verify_script__",
    "created_at": datetime.now(timezone.utc).isoformat(),
    "message":    "If you see this in Compass, everything works!",
    "status":     "verified",
}

try:
    result    = tasks_col.insert_one(test_doc)
    inserted_id = result.inserted_id
    print(f"  ✅ Step 2/3 — Document INSERTED")
    print(f"     _id : {inserted_id}\n")
except Exception as exc:
    print(f"  ❌ Insert failed: {exc}")
    client.close()
    sys.exit(1)

# ── 4. Read it back ────────────────────────────────────────────────────────────
try:
    fetched = tasks_col.find_one({"_id": inserted_id})
    assert fetched is not None, "Document not found after insert"
    assert fetched["title"]   == test_doc["title"]
    assert fetched["user_id"] == "__verify_script__"
    print(f"  ✅ Step 3/3 — Document READ BACK successfully")
    print(f"     title   : {fetched['title']}")
    print(f"     status  : {fetched['status']}")
    print(f"     message : {fetched['message']}\n")
except AssertionError as exc:
    print(f"  ❌ Read-back assertion failed: {exc}")
    client.close()
    sys.exit(1)
except Exception as exc:
    print(f"  ❌ Read failed: {exc}")
    client.close()
    sys.exit(1)

# ── 5. Final result ────────────────────────────────────────────────────────────
client.close()

print("=" * 60)
print("  ✅ SUCCESS: Database connected!")
print("  Open MongoDB Compass, click Refresh,")
print(f"  and check the '{DB_NAME}' → 'tasks' collection.")
print("=" * 60)
print(f"\n  Tip: filter by   {{ \"user_id\": \"__verify_script__\" }}")
print("       to find test documents quickly.\n")
