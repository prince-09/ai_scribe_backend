from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
# MongoDB Configuration
MONGO_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("MONGODB_DB")

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

client = AsyncIOMotorClient(MONGO_URI)
mongo_instance = client[DATABASE_NAME]

# Test the connection at startup
try:
    client.admin.command("ping")
    print("Connected to MongoDB!")
except ConnectionFailure:
    print("Failed to connect to MongoDB!")

