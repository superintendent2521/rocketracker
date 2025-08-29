from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from src.api.routes import api_router
from src.web.routes import html_router
app = FastAPI()

# Serve static files (CSS, JS, images, etc.)
app.mount("/styles", StaticFiles(directory="styles"), name="styles")
app.mount("/img", StaticFiles(directory="img"), name="img")
app.include_router(api_router, prefix="/api")
app.include_router(html_router)

# Custom 404 exception handler
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    with open("views/404.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=404)