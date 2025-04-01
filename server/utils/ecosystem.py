import asyncio
import aiofiles
from pydantic import BaseModel
from typing import Optional, List
from pathlib import Path
import json

class EcosystemApp(BaseModel):
    name: str
    script: str
    instances: Optional[str] = None
    watch: Optional[bool] = None
    args: Optional[List[str]] = None 
    log_file: Optional[str] = None

async def create_ecosystem_config(app: EcosystemApp):
    path = Path("server/browserList")
    config_content = generate_config_content(app)
    await write_config_file(path, app.name, config_content)
    print("File ecosystem.config.js đã được tạo!")

def generate_config_content(app: EcosystemApp) -> str:
    return json.dumps({
        "apps": [
            {
                "name": app.name,
                "script": app.script,
                "instances": app.instances or 'max',
                "watch": app.watch if app.watch is not None else True,
                "args": app.args or [],
                "log_file": app.log_file or ''
            }
        ]
    }, indent=4)

async def write_config_file(path: Path, name: str, content: str):
    async with aiofiles.open(f"{path.resolve()}/{name}.json", "w") as f:
        await f.write(content)

# Example usage
# example_app = EcosystemApp(
#     name="my-app",
#     script="index.js",
#     args=["--verbose", "--debug"],  # Example of list of arguments
#     log_file="/var/log/my-app.log"
# )

# asyncio.run(create_ecosystem_config(example_app))
