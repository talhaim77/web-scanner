import logging
from config import configure_logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.scan_router import router as scan_router
from views import router as template_router

configure_logging()
logger = logging.getLogger(__name__)
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(scan_router, tags=["Scan"])
app.include_router(template_router, tags=["Template"])

