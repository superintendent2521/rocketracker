# src/web/routes.py
"""
Web routes for serving HTML pages.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

html_router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


# Serve index.html
@html_router.get("/", response_class=HTMLResponse)
@limiter.limit("45/minute")
async def read_index(request: Request):  # pylint: disable=unused-argument
    """Serve the index page."""
    with open("views/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)


# Serve reporter.html
@html_router.get("/reporter", response_class=HTMLResponse)
@limiter.limit("45/minute")
async def read_reporter(request: Request):  # pylint: disable=unused-argument
    """Serve the reporter page."""
    with open("views/reporter.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)


# Serve viewer page
@html_router.get("/viewer", response_class=HTMLResponse)
@limiter.limit("45/minute")
async def read_viewer(request: Request):  # pylint: disable=unused-argument
    """Serve the viewer page."""
    with open("views/view.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)


@html_router.get("/launch/{launch_id}", response_class=HTMLResponse)
@limiter.limit("45/minute")
async def launch_page(
    launch_id: str, request: Request
):  # pylint: disable=unused-argument
    """Serve the launch page."""
    # launch_id is just for routing; JS will extract it from the URL
    with open("views/launch.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


# Serve 404 page
@html_router.get("/404", response_class=HTMLResponse)
@limiter.limit("45/minute")
async def read_404(request: Request):  # pylint: disable=unused-argument
    """Serve the 404 page."""
    with open("views/404.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=404)


# Serve fleet viewer page
@html_router.get("/fleet", response_class=HTMLResponse)
@limiter.limit("45/minute")
async def read_fleet(request: Request):  # pylint: disable=unused-argument
    """Serve the fleet viewer page."""
    with open("views/fleet.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)


# Serve individual booster page
@html_router.get("/fleet/booster/{booster_id}", response_class=HTMLResponse)
@limiter.limit("45/minute")
async def read_booster(
    booster_id: str, request: Request
):  # pylint: disable=unused-argument
    """Serve the individual booster page."""
    with open("views/booster.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)


# Serve individual ship page
@html_router.get("/fleet/ship/{ship_id}", response_class=HTMLResponse)
@limiter.limit("45/minute")
async def read_ship(ship_id: str, request: Request):  # pylint: disable=unused-argument
    """Serve the individual ship page."""
    with open("views/ship.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)


# Serve news page
@html_router.get("/news", response_class=HTMLResponse)
@limiter.limit("45/minute")
async def read_news(request: Request):  # pylint: disable=unused-argument
    """Serve the news page."""
    with open("views/news.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)


# Serve news reporter page
@html_router.get("/news/reporter", response_class=HTMLResponse)
@limiter.limit("45/minute")
async def read_news_reporter(request: Request):  # pylint: disable=unused-argument
    """Serve the news reporter page."""
    with open("views/newsreporter.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)


# Serve mission reporter page
@html_router.get("/missions/reporter", response_class=HTMLResponse)
@limiter.limit("45/minute")
async def read_mission_reporter(request: Request):  # pylint: disable=unused-argument
    """Serve the mission reporter page. Where they can report on launches."""
    with open("views/mission_reporter.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)
