import asyncio
from models import BrowserConfig

async def main():
    b = BrowserConfig(port=1234, config={"xxx": "l"})
    await b.save()  # Use await to call the asynchronous save method

# Run the async function
asyncio.run(main())