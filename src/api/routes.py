from fastapi import APIRouter
import fastapi
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import json
from datetime import datetime
from ..database import save
api_router = APIRouter()


# Data model for launch report
class LaunchReport(BaseModel):
    boosterNumber: str
    shipNumber: str
    boosterFlightCount: int
    shipFlightCount: int
    launchSite: str
    launchDate: str
    launchTime: str
    livestream: Optional[str] = None



# Handle launch report submissions
@api_router.post("/report/launch")
async def submit_launch_report(report: LaunchReport):

    report_data = report.dict()
    report_data["timestamp"] = datetime.now().isoformat()
    save(report_data)    #no db so print to console
    return {"message": "Launch report submitted successfully"}