from fastapi import APIRouter
from services.browser_service import BrowserService
from models import BrowserStart,BrowserDelete,BrowserStop

router = APIRouter(prefix="/browser")
browser_service = BrowserService()


@router.post("/create")
async def browser_create():
    return await browser_service.action_create()

@router.post("/start")
async def browser_start(body: BrowserStart):
    return await browser_service.action_start(identify=body.identify)

@router.post("/stop")
async def browser_stop(body:BrowserStop):
    return await browser_service.action_stop(identify=body.identify)

@router.delete("/delete")
async def browser_delete(body:BrowserDelete):
    return await browser_service.action_delete(identify=body.identify)

@router.get("/info/{identify}")
async def browser_info(identify: str):
    return await browser_service.get_info(identify=identify)

@router.get("/list")
async def browser_list():
    return await browser_service.get_list()