from fastapi import APIRouter
from services.browser import  BrowserService




browser_service = BrowserService()


router = APIRouter(prefix="/browser")


@router.get("/list")
async def get_browser_list():
    return await browser_service.get_browser_list()