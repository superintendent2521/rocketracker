from pymongo import AsyncMongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from bson import ObjectId
import os
from dotenv import load_dotenv
from pathlib import Path
from bson import ObjectId

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

async def get_specific_launch(launch_id: str):
    """Retrieve a specific launch by id string."""
    try:
        oid = ObjectId(launch_id)
    except Exception:
        # invalid 24-hex string
        return None

    launch = await collection.find_one({"_id": oid})
    if launch:
        # convert ObjectId back to a readable string before returning
        launch["_id"] = str(launch["_id"])
    return launch

async def get_missions_by_ship(ship_number: str):
    """Retrieve all missions completed by a specific ship"""
    try:
        cursor = collection.find({"shipNumber": ship_number})
        missions = await cursor.to_list(length=None)
        # Convert ObjectId to string for JSON serialization
        for mission in missions:
            mission["_id"] = str(mission["_id"])
        return missions
    except Exception as e:
        print(f"Error retrieving missions for ship {ship_number}: {e}")
        return []

async def get_missions_by_booster(booster_number: str):
    """Retrieve all missions completed by a specific booster"""
    try:
        cursor = collection.find({"boosterNumber": booster_number})
        missions = await cursor.to_list(length=None)
        # Convert ObjectId to string for JSON serialization
        for mission in missions:
            mission["_id"] = str(mission["_id"])
        return missions
    except Exception as e:
        print(f"Error retrieving missions for booster {booster_number}: {e}")
        return []
