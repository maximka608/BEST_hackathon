from bson import ObjectId
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from src.db.config import MONGODB_URL, MONGO_DB_NAME

client: MongoClient = None
db = None


def connect_to_mongo():
    global client, db
    client = MongoClient(
        MONGODB_URL,
        server_api=ServerApi("1")
    )

    db = client[MONGO_DB_NAME]


def close_mongo_connection():
    global client
    if client:
        client.close()


def get_mongo_db():
    if db is None:
        raise RuntimeError("MongoDB connection has not been initialized.")
    return db


def serialize_object_id(item):
    if isinstance(item, ObjectId):
        return str(item)
    if isinstance(item, dict):
        return {key: serialize_object_id(value) for key, value in item.items()}
    if isinstance(item, list):
        return [serialize_object_id(i) for i in item]
    return item


if __name__ == "__main__":
    connect_to_mongo()
    db = get_mongo_db()
    print("MongoDB connection established.")
    # Perform any operations with the database here
    close_mongo_connection()
    print("MongoDB connection closed.")

