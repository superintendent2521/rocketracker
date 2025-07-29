import fastapi
from fastapi import APIRouter, Request
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException
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
# Serve reporter.html
@html_router.get("/viewer", response_class=HTMLResponse)
async def read_reporter():
    with open("views/view.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)
@html_router.get("/launch/{launch_id}", response_class=HTMLResponse)
async def launch_page(launch_id: str):
    # launch_id is just for routing; JS will extract it from the URL
    with open("views/launch.html") as f:
        return HTMLResponse(f.read())
# Serve 404 page
@html_router.get("/404", response_class=HTMLResponse)
async def read_404():
    with open("views/404.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=404)
    