import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongo_uri")
MONGO_DB_NAME = "hackathon_lviv"
