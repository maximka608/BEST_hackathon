import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongo_url")
MONGO_DB_NAME = "hackathon_lviv"
