

import fastapi
from fastapi import APIRouter, Request
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import json
from datetime import datetime

html_router = APIRouter()



# Serve index.html
@html_router.get("/", response_class=HTMLResponse)
async def read_index():
    with open("views/index.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)



# Serve reporter.html
@html_router.get("/reporter", response_class=HTMLResponse)
async def read_reporter():
    with open("views/reporter.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)