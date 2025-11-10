import os
from typing import AsyncIterator
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv

load_dotenv()

_MONGO_CLIENT: AsyncIOMotorClient | None = None
_DB: AsyncIOMotorDatabase | None = None

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "car_api")

async def init_mongo() -> None:
    global _MONGO_CLIENT, _DB
    if _MONGO_CLIENT is None:
        _MONGO_CLIENT = AsyncIOMotorClient(MONGODB_URI)
        _DB = _MONGO_CLIENT[MONGODB_DB]
        # Ensure counter doc exists for integer IDs
        await _DB["counters"].update_one(
            {"_id": "car_id"},
            {"$setOnInsert": {"seq": 0}},
            upsert=True,
        )

async def shutdown_mongo() -> None:
    global _MONGO_CLIENT
    if _MONGO_CLIENT is not None:
        _MONGO_CLIENT.close()
        _MONGO_CLIENT = None

def get_db() -> AsyncIOMotorDatabase:
    if _DB is None:
        raise RuntimeError("Mongo not initialized. Call init_mongo() first.")
    return _DB

async def get_next_sequence(name: str) -> int:
    """
    Atomically increments and returns the next integer ID for a given sequence name.
    """
    db = get_db()
    doc = await db["counters"].find_one_and_update(
        {"_id": name},
        {"$inc": {"seq": 1}},
        return_document=True,
        upsert=True,
    )
    # If driver returns None on first upsert, fetch it
    if doc is None:
        doc = await db["counters"].find_one({"_id": name})
    return int(doc["seq"])
