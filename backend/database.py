from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "d2c_analytics")

client = None
database = None

async def init_db():
    global client, database
    client = AsyncIOMotorClient(MONGODB_URL, server_api=ServerApi('1'))
    database = client[DATABASE_NAME]
    
    # Test connection
    try:
        await client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

async def get_database():
    return database

async def close_db():
    if client:
        client.close()
