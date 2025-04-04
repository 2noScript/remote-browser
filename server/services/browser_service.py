from store import browser
from models import BrowserConfig
from pathlib import Path

_browser_lunchers_dir=Path("server/launcher.config/browsers")


class BrowserService:
    def __init__(self):
        pass
    
    async def action_start(self):
        return True

    async def action_stop(self):
        return True
    async def action_delete(self):
        return True
    async def get_info(self):
        return True
    async def get_list(self):
        return True