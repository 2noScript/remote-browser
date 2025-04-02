import aiofiles
from pathlib import Path


async def write_config_file(path: Path, name: str, content: str):
    async with aiofiles.open(f"{path.resolve()}/{name}.json", "w") as f:
        await f.write(content)