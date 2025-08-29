from fastapi import APIRouter, HTTPException

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, field_validator, validator
from typing import Optional
import json
import re

from datetime import datetime
from ..database import save, get_all_launches, get_specific_launch, get_missions_by_ship, get_missions_by_booster, save_news_post, get_all_news_posts, get_specific_news_post, save_mission, get_missions_by_launch
api_router = APIRouter()


class LaunchReport(BaseModel):
    boosterNumber: int
    shipNumber: int
    boosterFlightCount: int
    shipFlightCount: int
    launchSite: str
    launchDate: str
    launchTime: str
    livestream: Optional[str] = None
    
    @field_validator('boosterNumber', 'shipNumber', 'boosterFlightCount', 'shipFlightCount')
    def validate_positive_numbers(cls, v):
        if not isinstance(v, int) or v < 0:
            raise ValueError('must be a positive integer')
        return v

class NewsPost(BaseModel):
    title: str
    content: str
    author: str
    
    @field_validator('title')
    def validate_title(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('title is required')
        if len(v) > 100:
            raise ValueError('title must be 100 characters or less')
        return v.strip()
    
    @field_validator('content')
    def validate_content(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('content is required')
        if len(v) > 1000:
            raise ValueError('content must be 1000 characters or less')
        return v.strip()
    
    @field_validator('author')
    def validate_author(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('author is required')
        if len(v) > 50:
            raise ValueError('author must be 50 characters or less')
        return v.strip()

class MissionReport(BaseModel):
    launch_id: str
    mission_category: str
    starlink_count: Optional[int] = None
    payload_description: Optional[str] = None
    destination: Optional[str] = None
    additional_notes: Optional[str] = None
    
    @field_validator('mission_category')
    def validate_category(cls, v):
        valid_categories = {'starlink', 'propellant', 'cargo', 'crew', 'test', 'other'}
        if v not in valid_categories:
            raise ValueError('mission_category must be one of: starlink, propellant, cargo, crew, test, other')
        return v
    
    @field_validator('starlink_count')
    def validate_starlink_count(cls, v, info):
        values = info.data
        if values.get('mission_category') == 'starlink':
            if v is None or v < 1:
                raise ValueError('starlink_count is required for starlink missions and must be positive')
        return v
    
    @field_validator('payload_description', 'destination')
    def validate_general_fields(cls, v, info):
        values = info.data
        field_name = info.field_name
        category = values.get('mission_category')
        if category and category not in ['starlink', 'propellant']:
            if not v or len(v.strip()) == 0:
                raise ValueError(f'{field_name} is required for {category} missions')
# Handle launch report submissions
@api_router.post("/report/launch") #await because db operation
async def submit_launch_report(report: LaunchReport):

    report_data = report.dict()
    report_data["timestamp"] = datetime.now().isoformat()
    await save(report_data)    #save to db, uses await however not here, in db module
    return {"message": "Launch report submitted successfully"}
@api_router.get("/getlaunches")
async def get_launches():
    """Get all launch reports"""
    try:
        launches = await get_all_launches()
        # Convert ObjectId to string for JSON serialization
        for launch in launches:
            launch['_id'] = str(launch['_id'])
        return launches  # Return array directly
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#code of doom an dispair
@api_router.get("/getlaunches/{launch_id}")
async def get_id_specific_launch(launch_id: str):
    try:
        launches = await get_specific_launch(launch_id)   # call your service/repo
        return launches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/mission/ship/{id}")
async def get_missions_by_ship_id(id: str):
    """Get all missions completed by a specific ship using its assigned number"""
    try:
        missions = await get_missions_by_ship(id)
        return missions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/mission/booster/{id}")
async def get_missions_by_booster_id(id: str):
    """Get all missions completed by a specific booster using its assigned number"""
    try:
        missions = await get_missions_by_booster(id)
        return missions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# News API endpoints
@api_router.post("/news/post")
async def submit_news_post(post: NewsPost):
    """Submit a new news post"""
    try:
        post_data = post.dict()
        post_data["timestamp"] = datetime.now().isoformat()
        result = await save_news_post(post_data)
        if result:
            return {"message": "News post submitted successfully", "id": str(result.inserted_id)}
        else:
            raise HTTPException(status_code=500, detail="Failed to save news post")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/news")
async def get_news_posts():
    """Get all news posts"""
    try:
        posts = await get_all_news_posts()
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/news/{post_id}")
async def get_news_post(post_id: str):
    """Get a specific news post by ID"""
    try:
        post = await get_specific_news_post(post_id)
        if post:
            return post
        else:
            raise HTTPException(status_code=404, detail="News post not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mission API endpoints
@api_router.post("/missions")
async def submit_mission(mission: MissionReport):
    """Submit a new mission report"""
    try:
        mission_data = mission.dict()
        mission_data["timestamp"] = datetime.now().isoformat()
        result = await save_mission(mission_data)
        if result:
            return {"message": "Mission submitted successfully", "id": str(result.inserted_id)}
        else:
            raise HTTPException(status_code=500, detail="Failed to save mission")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/missions/{launch_id}")
async def get_missions_for_launch(launch_id: str):
    """Get all missions for a specific launch"""
    try:
        missions = await get_missions_by_launch(launch_id)
        return missions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
