"""This module handles API routes."""

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.exceptions import HTTPException
from slowapi.errors import RateLimitExceeded
from loguru import logger
from src.api.routes import api_router, limiter
from src.web.routes import html_router
from datetime import datetime
logger_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # Windows is a bitch and doesnt like semicolons in files.
logger.add(f"logs/app_{logger_date}.log", rotation="10 MB", retention="10 days", level="INFO", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

logger.add("logs/app.log", rotation="10 MB", retention="10 days", level="INFO", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

app = FastAPI()
app.state.limiter = limiter

from src.database import test_motor_connection

@app.on_event("startup")
async def startup_event():
    connected = await test_motor_connection()
    if not connected:
        logger.warning("MongoDB connection failed, but continuing startup.")


async def custom_rate_limit_handler(_request: Request, _exc: RateLimitExceeded):
    """Custom handler for rate limit exceeded. Returns HTML page."""
    with open("views/429.html", "r", encoding="utf-8") as file:
        content = file.read()
        return HTMLResponse(content=content, status_code=429)
ENV_PATH = ".env"
load_dotenv(dotenv_path=ENV_PATH)
logger.info("Loaded environment variables from .env file")

if os.getenv('RATELIMIT', 'true').lower() == 'true':
    app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)
    logger.info("Rate limiting is enabled")
else:
    logger.info("Rate limiting is disabled")
# Serve static files (CSS, JS, images, etc.)
app.mount("/styles", StaticFiles(directory="styles"), name="styles")
app.mount("/img", StaticFiles(directory="img"), name="img")
app.include_router(api_router, prefix="/api")
app.include_router(html_router)


async def custom_404_handler(_request: Request, _exc: HTTPException):
    """Custom handler for 404 errors. Returns a static HTML page."""
    with open("views/404.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=404)
