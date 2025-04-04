import asyncio
from models import BrowserConfig
from utils.commands import CamoufoxCommand
import time

async def main():
    br = BrowserConfig(port=4002, config={"headless": False, "debug": True})
    cm=CamoufoxCommand(br)
    await cm.start()
    # a=await cm.stop()


# Run the async function
asyncio.run(main())