import asyncio
import aiofiles
from pydantic import BaseModel
from typing import Optional, Dict
from typing import Optional, List

class EcosystemApp(BaseModel):
    name: str
    script: str
    instances: Optional[str] = None
    watch: Optional[bool] = None
    args: Optional[List[str]] = None 
    log_file: Optional[str] = None

async def create_ecosystem_config(app: EcosystemApp):
    config_content = f"""{{
        "apps": [
            {{
                "name": "{app.name}",
                "script": "{app.script}",
                "instances": "{app.instances or 'max'}",
                "watch": {str(app.watch).lower() if app.watch is not None else 'true'},
                "args": {app.args or []},  # Updated to handle list
                "log_file": "{app.log_file or ''}"
            }}
        ]
    }}"""
    
    async with aiofiles.open("ecosystem.json", "w") as f:
        await f.write(config_content)

    print("File ecosystem.config.js đã được tạo!")

# Example usage
# example_app = EcosystemApp(
#     name="my-app",
#     script="index.js",
#     args=["--verbose", "--debug"],  # Example of list of arguments
#     log_file="/var/log/my-app.log"
# )

# asyncio.run(create_ecosystem_config(example_app))
