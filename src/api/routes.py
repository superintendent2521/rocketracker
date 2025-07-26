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
from ..database import save
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
@api_router.post("/report/launch")
async def submit_launch_report(report: LaunchReport):

    report_data = report.dict()
    report_data["timestamp"] = datetime.now().isoformat()
    save(report_data)    #no db so print to console
    return {"message": "Launch report submitted successfully"}