from fastapi import APIRouter
import fastapi
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, validator
from typing import Optional
import json
import re

from datetime import datetime
from ..database import save, get_all_launches
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


# Handle launch report submissions
@api_router.post("/report/launch") #await because db operation
async def submit_launch_report(report: LaunchReport):

    report_data = report.dict()
    report_data["timestamp"] = datetime.now().isoformat()
    save(report_data)    #save to db, uses await however not here, in db module
    return {"message": "Launch report submitted successfully"}

@api_router.get("/api/getlaunches")
async def recieve_launch_total():
    launch_total = await get_all_launches() # await because database operation
    return {"message": f"{launch_total}"}