

from fastapi import APIRouter

router = APIRouter(prefix="browser")

@router.get("/start")
async def browser_start():
    return {"message": "pong"}

@router.get("/start")
async def browser_stop():
    return {"message": "pong"}

@router.get("/delete")
async def browser_delete():
    return {"message": "pong"}

@router.get("/info")
async def browser_info():
    return {"message": "pong"}

@router.get("/list")
async def browser_list():
    return {"message": "pong"}