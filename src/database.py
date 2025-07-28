from pymongo import AsyncMongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from parent directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Initialize the MongoDB client
client = AsyncIOMotorClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('MONGODB_DB_NAME')]
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

async def get_specific_launch(launch_id):
    """Retrieve a certain launch"""
    try:
        launch = await collection.find_one({"_id": launch_id})
        return launch
    except Exception as e:
        print(f"Error retrieving launch: {e}")
        return None
