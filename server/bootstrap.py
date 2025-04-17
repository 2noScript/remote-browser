from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from constant import DEV
from db import init_database
from pathlib import Path

from routers.ping import router as ping_router
from routers import router as browser_router



app = FastAPI()

app.include_router(ping_router)
app.include_router(browser_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.mount("/", StaticFiles(directory="ui/dist", html=True), name="static")

if __name__ == "__main__":
    if not Path("database.db").exists():
        init_database()
    uvicorn.run("bootstrap:app", host="0.0.0.0", port=5008, reload=bool(DEV))
