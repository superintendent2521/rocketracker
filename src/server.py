from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typing import union
app = FastAPI()
app.mount("/styles", StaticFiles(directory="styles"), name="static")