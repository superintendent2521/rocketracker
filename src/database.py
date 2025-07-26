from pymongo import AsyncMongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

# Initialize the MongoDB client
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client.your_database_name
collection = db.launch_reports

async def save(launch_report):
    """Save a launch report to MongoDB"""
    try:
        result = await collection.insert_one(launch_report)
        print(f"Saved report with id: {result.inserted_id}")
        return result
    except Exception as e:
        print(f"Error saving report: {e}")
        return None

async def get_all_launches():
    """Retrieve all launch reports"""
    try:
        cursor = collection.find({})
        launches = await cursor.to_list(length=None)
        return launches
    except Exception as e:
        print(f"Error retrieving launches: {e}")
        return []
