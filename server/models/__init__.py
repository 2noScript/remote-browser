from pydantic import BaseModel, Field
import uuid
from pathlib import Path


_browser_lunchers_dir=Path("server/launcher.config/browsers")

class BrowserConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    config: dict = {}
    port: int

    def parse(self):
        return {
            **self.config,
            "port": self.port,
            "ws_path":self.id,
        }


class BrowserStart(BaseModel):
    identify: str
class BrowserDelete(BaseModel):
    identify: str
class BrowserStop(BaseModel):
    identify: str

















