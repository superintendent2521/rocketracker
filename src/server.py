import fastapi
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import json
from datetime import datetime

app = FastAPI()

# Serve static files (CSS, JS, images, etc.)
app.mount("/styles", StaticFiles(directory="styles"), name="styles")

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

# Serve index.html
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)

# Handle launch report submissions
@app.post("/report/launch")
async def submit_launch_report(report: LaunchReport):

    report_data = report.dict()
    report_data["timestamp"] = datetime.now().isoformat()
    #no db so print to console
    print("Received launch report:", report_data)
    return {"message": "Launch report submitted successfully"}

# Serve reporter.html
@app.get("/reporter", response_class=HTMLResponse)
async def read_reporter():
    with open("reporter.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)