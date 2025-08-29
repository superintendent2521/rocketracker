"""This module handles API routes."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.exceptions import HTTPException
from src.api.routes import api_router
from src.web.routes import html_router

app = FastAPI()

# Serve static files (CSS, JS, images, etc.)
app.mount("/styles", StaticFiles(directory="styles"), name="styles")
app.mount("/img", StaticFiles(directory="img"), name="img")
app.include_router(api_router, prefix="/api")
app.include_router(html_router)


async def custom_404_handler(_request: Request, _exc: HTTPException):
    """Custom handler for 404 errors. Returns a static HTML page."""
    with open("views/404.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=404)
