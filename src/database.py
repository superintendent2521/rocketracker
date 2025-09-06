"""Database layer for MongoDB access.

Handles connections to MongoDB and provides functions to
save and retrieve launch reports, news posts, and mission data.
"""

import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv
from pymongo.errors import PyMongoError

# Load environment variables from parent directory
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Initialize the MongoDB client
client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("MONGODB_DB_NAME")]
collection = db.launch_reports
news_collection = db.news_posts
missions_collection = db.missions

# Test connection to MongoDB
async def test_motor_connection():
    try:
        await client.admin.command("ping")
        print("✅ Connected to MongoDB")
    except ServerSelectionTimeoutError as e:
        print("❌ Could not connect:", e)

async def save(launch_report):
    """Save a launch report to MongoDB"""
    try:
        result = await collection.insert_one(launch_report)
        print(f"Saved report with id: {result.inserted_id}")
        return result
    except PyMongoError as e:
        print(f"Database error saving report: {e}")
        return None


async def get_all_launches():
    """Retrieve all launch reports"""
    try:
        cursor = collection.find({})
        launches = await cursor.to_list(length=None)
        return launches
    except PyMongoError as e:
        print(f"Database error retrieving launches: {e}")
        return []


async def get_specific_launch(launch_id: str):
    """Retrieve a specific launch by id string."""
    try:
        oid = ObjectId(launch_id)
    except (TypeError, ValueError):  # invalid ObjectId format
        return None

    launch = await collection.find_one({"_id": oid})
    if launch:
        launch["_id"] = str(launch["_id"])  # convert for JSON serialization
    return launch


async def get_missions_by_ship(ship_number: str):
    """Retrieve all missions completed by a specific ship"""
    try:
        ship_number_int = int(ship_number)
        cursor = collection.find({"shipNumber": ship_number_int})
        missions = await cursor.to_list(length=None)
        for mission in missions:
            mission["_id"] = str(mission["_id"])
        return missions
    except ValueError:
        print(f"Invalid ship number format: {ship_number}")
        return []
    except PyMongoError as e:
        print(f"Database error retrieving missions for ship {ship_number}: {e}")
        return []


async def get_missions_by_booster(booster_number: str):
    """Retrieve all missions completed by a specific booster"""
    try:
        booster_number_int = int(booster_number)
        cursor = collection.find({"boosterNumber": booster_number_int})
        missions = await cursor.to_list(length=None)
        for mission in missions:
            mission["_id"] = str(mission["_id"])
        return missions
    except ValueError:
        print(f"Invalid booster number format: {booster_number}")
        return []
    except PyMongoError as e:
        print(f"Database error retrieving missions for booster {booster_number}: {e}")
        return []


async def save_news_post(news_post):
    """Save a news post to MongoDB"""
    try:
        result = await news_collection.insert_one(news_post)
        print(f"Saved news post with id: {result.inserted_id}")
        return result
    except PyMongoError as e:
        print(f"Database error saving news post: {e}")
        return None


async def get_all_news_posts():
    """Retrieve all news posts, sorted by newest first"""
    try:
        cursor = news_collection.find({}).sort("timestamp", -1)
        posts = await cursor.to_list(length=None)
        for post in posts:
            post["_id"] = str(post["_id"])
        return posts
    except PyMongoError as e:
        print(f"Database error retrieving news posts: {e}")
        return []


async def get_specific_news_post(post_id: str):
    """Retrieve a specific news post by id string"""
    try:
        oid = ObjectId(post_id)
    except (TypeError, ValueError):  # invalid ObjectId
        return None

    post = await news_collection.find_one({"_id": oid})
    if post:
        post["_id"] = str(post["_id"])
    return post


async def save_mission(mission_data):
    """Save a mission report to MongoDB"""
    try:
        result = await missions_collection.insert_one(mission_data)
        print(f"Saved mission with id: {result.inserted_id}")
        return result
    except PyMongoError as e:
        print(f"Database error saving mission: {e}")
        return None


async def get_missions_by_launch(launch_id: str):
    """Retrieve all missions for a specific launch"""
    try:
        cursor = missions_collection.find({"launch_id": launch_id})
        missions = await cursor.to_list(length=None)
        for mission in missions:
            mission["_id"] = str(mission["_id"])
        return missions
    except PyMongoError as e:
        print(f"Database error retrieving missions for launch {launch_id}: {e}")
        return []
