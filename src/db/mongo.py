from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

from src.db.config import MONGO_URI, MONGO_DB_NAME

client: AsyncIOMotorClient = None
db = None


async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(MONGO_URI, server_api=ServerApi("1"))
    db = client[MONGO_DB_NAME]


async def close_mongo_connection():
    client.close()
