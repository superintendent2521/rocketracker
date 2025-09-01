# src/web/routes.py
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
html_router = APIRouter()


# Serve index.html
@html_router.get("/", response_class=HTMLResponse)

async def read_index():
    with open("views/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)


# Serve reporter.html
@html_router.get("/reporter", response_class=HTMLResponse)
async def read_reporter():
    with open("views/reporter.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)


# Serve viewer page
@html_router.get("/viewer", response_class=HTMLResponse)
async def read_viewer():
    with open("views/view.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)


@html_router.get("/launch/{launch_id}", response_class=HTMLResponse)
async def launch_page(launch_id: str):
    # launch_id is just for routing; JS will extract it from the URL
    with open("views/launch.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


# Serve 404 page
@html_router.get("/404", response_class=HTMLResponse)
async def read_404():
    with open("views/404.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=404)


# Serve fleet viewer page
@html_router.get("/fleet", response_class=HTMLResponse)
async def read_fleet():
    """Serve the fleet viewer page."""
    with open("views/fleet.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)


# Serve individual booster page
@html_router.get("/fleet/booster/{booster_id}", response_class=HTMLResponse)
async def read_booster(booster_id: str):
    """Serve the individual booster page."""
    with open("views/booster.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)


# Serve individual ship page
@html_router.get("/fleet/ship/{ship_id}", response_class=HTMLResponse)
async def read_ship(ship_id: str):
    """Serve the individual ship page."""
    with open("views/ship.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)


# Serve news page
@html_router.get("/news", response_class=HTMLResponse)
async def read_news():
    """Serve the news page."""
    with open("views/news.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)


# Serve news reporter page
@html_router.get("/news/reporter", response_class=HTMLResponse)
async def read_news_reporter():
    """Serve the news reporter page."""
    with open("views/newsreporter.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)


# Serve mission reporter page
@html_router.get("/missions/reporter", response_class=HTMLResponse)
async def read_mission_reporter():
    """Serve the mission reporter page. Where they can report on launches."""
    with open("views/mission_reporter.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)
