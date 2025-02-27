from fastapi import FastAPI
from routers.scan_router import router as scan_router
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(scan_router, tags=["Scan"])

