from pydantic import BaseModel, Field
from utils.helper import write_config_file
import json
import uuid
from pathlib import Path


_browser_lunchers_dir=Path("server/launcher.config/browsers")

class BrowserConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    config: dict = {}
    port: int
    
    async def save(self):
        browser_config = json.dumps(**self.parse())
        await write_config_file(path=_browser_lunchers_dir,name=self.id,content=browser_config)
    def parse(self):
        return {
            **self.config,
            "port": self.port,
            "ws_path":self.id,
        }
















