import logging
from config import configure_logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.scan_router import router as scan_router
from views import router as template_router

configure_logging()
logger = logging.getLogger(__name__)
app = FastAPI(
    title="Web Metadata Scanner",
    description="This is a WebScanner API",
    version="1.0.0",
    redoc_url="/redoc",
)
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(scan_router, tags=["Scan"])
app.include_router(template_router, tags=["Template"])
