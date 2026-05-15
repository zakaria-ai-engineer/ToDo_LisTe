"""
database.py — MongoDB connection and collection accessors.
"""
from pymongo import MongoClient
from pymongo.collection import Collection
from app.config.settings import settings


class Database:
    client: MongoClient = None

    @classmethod
    def connect(cls):
        cls.client = MongoClient(settings.MONGODB_URL)

    @classmethod
    def disconnect(cls):
        if cls.client:
            cls.client.close()

    @classmethod
    def get_db(cls):
        return cls.client[settings.DB_NAME]


def get_tasks_collection() -> Collection:
    return Database.get_db()["tasks"]


def get_users_collection() -> Collection:
    return Database.get_db()["users"]
