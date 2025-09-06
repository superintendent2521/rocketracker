"""
API routes module for RocketTracker.

Provides API endpoints for launch reports, news posts, and mission reports.
Handles CRUD operations for flight data, news, and mission tracking.
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, field_validator
from slowapi import Limiter
from slowapi.util import get_remote_address
from loguru import logger
from ..database import (
    save,
    get_all_launches,
    get_specific_launch,
    get_missions_by_ship,
    get_missions_by_booster,
    save_news_post,
    get_all_news_posts,
    get_specific_news_post,
    save_mission,
    get_missions_by_launch,
)  # noqa: E0402

api_router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


class LaunchReport(BaseModel):
    """Model for launch report submissions."""
    boosterNumber: int
    shipNumber: int
    boosterFlightCount: int
    shipFlightCount: int
    launchSite: str
    launchDate: str
    launchTime: str
    livestream: Optional[str] = None

    @field_validator(
        "boosterNumber", "shipNumber", "boosterFlightCount", "shipFlightCount"
    )
    @classmethod
    def validate_positive_numbers(cls, v):
        """Validate that the value is a positive integer."""
        if not isinstance(v, int) or v < 0:
            raise ValueError("must be a positive integer")
        return v


class NewsPost(BaseModel):
    """Model for news post submissions."""
    title: str
    content: str
    author: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        """Validate the title field."""
        if not v or len(v.strip()) == 0:
            raise ValueError("title is required")
        if len(v) > 100:
            raise ValueError("title must be 100 characters or less")
        return v.strip()

    @field_validator("content")
    @classmethod
    def validate_content(cls, v):
        """Validate the content field."""
        if not v or len(v.strip()) == 0:
            raise ValueError("content is required")
        if len(v) > 1000:
            raise ValueError("content must be 1000 characters or less")
        return v.strip()

    @field_validator("author")
    @classmethod
    def validate_author(cls, v):
        """Validate the author field."""
        if not v or len(v.strip()) == 0:
            raise ValueError("author is required")
        if len(v) > 50:
            raise ValueError("author must be 50 characters or less")
        return v.strip()


class MissionReport(BaseModel):
    """Model for mission report submissions."""
    launch_id: str
    mission_category: str
    starlink_count: Optional[int] = None
    payload_description: Optional[str] = None
    destination: Optional[str] = None
    additional_notes: Optional[str] = None

    @field_validator("mission_category")
    @classmethod
    def validate_category(cls, v):
        """Validate the mission category."""
        valid_categories = {"starlink", "propellant", "cargo", "crew", "test", "other"}
        if v not in valid_categories:
            raise ValueError(
                "mission_category must be one of: starlink, propellant, "
                "cargo, crew, test, other"
            )
        return v

    @field_validator("starlink_count")
    @classmethod
    def validate_starlink_count(cls, v, info):
        """Validate the starlink count for starlink missions."""
        values = info.data
        if values.get("mission_category") == "starlink":
            if v is None or v < 1:
                raise ValueError(
                    "starlink_count is required for starlink missions and must be positive"
                )
        return v

    @field_validator("payload_description", "destination")
    @classmethod
    def validate_general_fields(cls, v, info):
        """Validate general fields based on mission category."""
        values = info.data
        field_name = info.field_name
        category = values.get("mission_category")
        if category and category not in ["starlink", "propellant"]:
            if not v or len(v.strip()) == 0:
                raise ValueError(f"{field_name} is required for {category} missions")


# Handle launch report submissions
@api_router.post("/report/launch")  # await because db operation
@limiter.limit("5/minute")  # rate limit to 5 per minute per IP
async def submit_launch_report(report: LaunchReport, request: Request):
    """Submit a launch report."""
    report_data = report.dict()
    report_data["timestamp"] = datetime.now().isoformat()
    await save(report_data)  # save to db, uses await however not here, in db module
    logger.info("Launch report submitted successfully")
    return {"message": "Launch report submitted successfully"}


@api_router.get("/getlaunches")
@limiter.limit("45/minute")
async def get_launches(request: Request):
    """Get all launch reports"""
    try:
        launches = await get_all_launches()
        # Convert ObjectId to string for JSON serialization
        for launch in launches:
            launch["_id"] = str(launch["_id"])
        logger.info("Retrieved all launches")
        return launches  # Return array directly
    except Exception as e:
        logger.error(f"Error retrieving launches: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


# code of doom an dispair
@api_router.get("/getlaunches/{launch_id}")
@limiter.limit("30/minute")
async def get_id_specific_launch(launch_id: str, request: Request):
    """Get a specific launch by ID."""
    try:
        launches = await get_specific_launch(launch_id)  # call your service/repo
        if launches:
            logger.info(f"Retrieved specific launch {launch_id}")
        return launches
    except Exception as e:
        logger.error(f"Error retrieving specific launch {launch_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@api_router.get("/mission/ship/{ship_id}")
@limiter.limit("30/minute")
async def get_missions_by_ship_id(ship_id: str, request: Request):
    """Get all missions completed by a specific ship using its assigned number"""
    try:
        missions = await get_missions_by_ship(ship_id)
        logger.info(f"Retrieved missions for ship {ship_id}")
        return missions
    except Exception as e:
        logger.error(f"Error retrieving missions for ship {ship_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@api_router.get("/mission/booster/{booster_id}")
@limiter.limit("30/minute")
async def get_missions_by_booster_id(booster_id: str, request: Request):
    """Get all missions completed by a specific booster using its assigned number"""
    try:
        missions = await get_missions_by_booster(booster_id)
        logger.info(f"Retrieved missions for booster {booster_id}")
        return missions
    except Exception as e:
        logger.error(f"Error retrieving missions for booster {booster_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


# News API endpoints
@api_router.post("/news/post")
@limiter.limit("5/minute")
async def submit_news_post(post: NewsPost, request: Request):
    """Submit a new news post"""
    try:
        post_data = post.dict()
        post_data["timestamp"] = datetime.now().isoformat()
        result = await save_news_post(post_data)
        if result:
            logger.info(f"News post submitted successfully with id: {result.inserted_id}")
            return {
                "message": "News post submitted successfully",
                "id": str(result.inserted_id),
            }
        raise HTTPException(status_code=500, detail="Failed to save news post")
    except Exception as e:
        logger.error(f"Error submitting news post: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@api_router.get("/news")
@limiter.limit("20/minute")
async def get_news_posts(request: Request):
    """Get all news posts"""
    try:
        posts = await get_all_news_posts()
        logger.info("Retrieved all news posts")
        return posts
    except Exception as e:
        logger.error(f"Error retrieving news posts: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@api_router.get("/news/{post_id}")
@limiter.limit("30/minute")
async def get_news_post(post_id: str, request: Request):
    """Get a specific news post by ID"""
    try:
        post = await get_specific_news_post(post_id)
        if post:
            logger.info(f"Retrieved specific news post {post_id}")
            return post
        raise HTTPException(status_code=404, detail="News post not found")
    except Exception as e:
        logger.error(f"Error retrieving specific news post {post_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


# Mission API endpoints
@api_router.post("/missions")
@limiter.limit("5/minute")
async def submit_mission(mission: MissionReport, request: Request):
    """Submit a new mission report"""
    try:
        mission_data = mission.dict()
        mission_data["timestamp"] = datetime.now().isoformat()
        result = await save_mission(mission_data)
        if result:
            logger.info(f"Mission submitted successfully with id: {result.inserted_id}")
            return {
                "message": "Mission submitted successfully",
                "id": str(result.inserted_id),
            }
        raise HTTPException(status_code=500, detail="Failed to save mission")
    except Exception as e:
        logger.error(f"Error submitting mission: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@api_router.get("/missions/{launch_id}")
@limiter.limit("30/minute")
async def get_missions_for_launch(launch_id: str, request: Request):
    """Get all missions for a specific launch, for refueling missions. like Mars or HLS"""
    try:
        missions = await get_missions_by_launch(launch_id)
        logger.info(f"Retrieved missions for launch {launch_id}")
        return missions
    except Exception as e:
        logger.error(f"Error retrieving missions for launch {launch_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e
