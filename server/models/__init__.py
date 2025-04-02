from pydantic import BaseModel, Field
from utils.helper import write_config_file
import json
import uuid
from pathlib import Path


_browser_lunchers_dir=Path("server/launcher.config/browsers")



# from playwright.sync_api import sync_playwright

# with sync_playwright() as p:
#     browser = p.firefox.connect('ws://localhost:8080/port/id')
#     page = browser.new_page()
#     page.goto('https://example.com')  # Change this to the URL of your choice
#     title = page.title()
#     print(f"Page title: {title}")

class BrowserConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    config: dict = {}
    port: int
    
    async def save(self):
        browser_config = json.dumps({
            **self.config,
            "port": self.port,
            "ws_path":self.id,

        })
        await write_config_file(path=_browser_lunchers_dir,name=self.id,content=browser_config)
















