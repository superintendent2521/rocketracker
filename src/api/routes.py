from fastapi import APIRouter, HTTPException
import fastapi
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, validator
from typing import Optional
import json
import re

from datetime import datetime
from ..database import save, get_all_launches, get_specific_launch
api_router = APIRouter()


class LaunchReport(BaseModel):
    boosterNumber: str
    shipNumber: str
    boosterFlightCount: int
    shipFlightCount: int
    launchSite: str
    launchDate: str
    launchTime: str
    livestream: Optional[str] = None
    
    @validator('boosterNumber', 'shipNumber')
    def validate_alphanumeric(cls, v):
        if not re.match("^[a-zA-Z0-9]+$", v):
            raise ValueError('must be alphanumeric')
        return v

# dont add /api/ it already gives you a /api/ prefix
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