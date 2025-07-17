import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def get_database():
    return db.database

async def connect_to_mongo():
    """Create database connection"""
    db.client = AsyncIOMotorClient(
        os.getenv("MONGODB_URL", "mongodb://localhost:27017"),
        server_api=ServerApi('1')
    )
    db.database = db.client[os.getenv("DATABASE_NAME", "d2c_analytics")]
    
    # Test the connection
    try:
        await db.client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB!")

async def get_collection(collection_name: str):
    """Get a collection from the database"""
    database = await get_database()
    return database[collection_name]
