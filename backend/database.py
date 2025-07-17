from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "d2c_analytics")

client = None
database = None

async def init_db():
    global client, database
    client = AsyncIOMotorClient(MONGODB_URL)
    database = client[DATABASE_NAME]
    
    # Create indexes
    await database.users.create_index("email", unique=True)
    await database.user_integrations.create_index([("user_id", ASCENDING), ("platform", ASCENDING)])
    await database.analytics_data.create_index([("user_id", ASCENDING), ("date", DESCENDING)])
    
    print("Database initialized successfully")

async def get_database():
    return database

async def close_db():
    if client:
        client.close()
