from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.staticfiles import StaticFiles
from constant.config import DEV

from routers.ping import router as ping_router
from routers.browser import router as browser_router



app = FastAPI()

app.include_router(ping_router)
app.include_router(browser_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.mount("/", StaticFiles(directory="ui/dist", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("bootstrap:app", host="0.0.0.0", port=3000, reload=DEV)