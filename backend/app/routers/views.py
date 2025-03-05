from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="static/templates")

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse(url="/home")


@router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
