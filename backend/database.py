import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "d2c_analytics")

client: AsyncIOMotorClient = None
database = None

async def connect_to_mongo():
    """Create database connection"""
    global client, database
    client = AsyncIOMotorClient(MONGODB_URL)
    database = client[DATABASE_NAME]
    print(f"Connected to MongoDB at {MONGODB_URL}")

async def close_mongo_connection():
    """Close database connection"""
    global client
    if client:
        client.close()
        print("Disconnected from MongoDB")

def get_database():
    return database
