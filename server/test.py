import asyncio
from utils.ecosystem import create_ecosystem_config,EcosystemApp

option = {
    "name": "hello",
    "script": "test.py",
    "instances": "max",
    "watch": True,
    "args": ["test", "test"],
    "log_file": "test.log"
}

option = EcosystemApp(**option)
async def main():
    await create_ecosystem_config(option)

# Run the async function
asyncio.run(main())