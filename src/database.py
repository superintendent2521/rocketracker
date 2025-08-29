from pymongo import AsyncMongoClient
from motor.motor_asyncio import AsyncIOMotorClient
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
news_collection = db.news_posts

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
        # Convert string to int for database query
        ship_number_int = int(ship_number)
        cursor = collection.find({"shipNumber": ship_number_int})
        missions = await cursor.to_list(length=None)
        # Convert ObjectId to string for JSON serialization
        for mission in missions:
            mission["_id"] = str(mission["_id"])
        return missions
    except ValueError:
        # Handle case where ship_number is not a valid integer
        print(f"Invalid ship number format: {ship_number}")
        return []
    except Exception as e:
        print(f"Error retrieving missions for ship {ship_number}: {e}")
        return []

async def get_missions_by_booster(booster_number: str):
    """Retrieve all missions completed by a specific booster"""
    try:
        # Convert string to int for database query
        booster_number_int = int(booster_number)
        cursor = collection.find({"boosterNumber": booster_number_int})
        missions = await cursor.to_list(length=None)
        # Convert ObjectId to string for JSON serialization
        for mission in missions:
            mission["_id"] = str(mission["_id"])
        return missions
    except ValueError:
        # Handle case where booster_number is not a valid integer
        print(f"Invalid booster number format: {booster_number}")
        return []
    except Exception as e:
        print(f"Error retrieving missions for booster {booster_number}: {e}")
        return []

# News-related database functions
async def save_news_post(news_post):
    """Save a news post to MongoDB"""
    try:
        result = await news_collection.insert_one(news_post)
        print(f"Saved news post with id: {result.inserted_id}")
        return result
    except Exception as e:
        print(f"Error saving news post: {e}")
        return None

async def get_all_news_posts():
    """Retrieve all news posts, sorted by newest first"""
    try:
        cursor = news_collection.find({}).sort("timestamp", -1)
        posts = await cursor.to_list(length=None)
        # Convert ObjectId to string for JSON serialization
        for post in posts:
            post["_id"] = str(post["_id"])
        return posts
    except Exception as e:
        print(f"Error retrieving news posts: {e}")
        return []

async def get_specific_news_post(post_id: str):
    """Retrieve a specific news post by id string"""
    try:
        oid = ObjectId(post_id)
    except Exception:
        # invalid 24-hex string
        return None

    post = await news_collection.find_one({"_id": oid})
    if post:
        # convert ObjectId back to a readable string before returning
        post["_id"] = str(post["_id"])
    return post

# Mission-related database functions
missions_collection = db.missions

async def save_mission(mission_data):
    """Save a mission report to MongoDB"""
    try:
        result = await missions_collection.insert_one(mission_data)
        print(f"Saved mission with id: {result.inserted_id}")
        return result
    except Exception as e:
        print(f"Error saving mission: {e}")
        return None

async def get_missions_by_launch(launch_id: str):
    """Retrieve all missions for a specific launch"""
    try:
        cursor = missions_collection.find({"launch_id": launch_id})
        missions = await cursor.to_list(length=None)
        # Convert ObjectId to string for JSON serialization
        for mission in missions:
            mission["_id"] = str(mission["_id"])
        return missions
    except Exception as e:
        print(f"Error retrieving missions for launch {launch_id}: {e}")
        return []
