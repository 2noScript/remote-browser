from pm2 import PM2, AioPM2
import asyncio

pm2 = PM2()
aiopm2 = AioPM2()



# Async Methods
async def pm2_manager():
    # List all processes
    processes = await aiopm2.list()
    print(processes)

    # Start a process
    await aiopm2.start(
        path="/Users/2noscript/workspace/project/remote-browser-server/server/ecosystem/browser_test.json",
    )

    # # Restart a process
    # await aiopm2.restart(name="Script-Name")  # or pid=12345 or pm_id=1

    # # Stop a process
    # await aiopm2.stop(name="Script-Name")  # or pid=12345 or pm_id=1

    # # Delete a process
    # await aiopm2.delete(name="Script-Name")  # or pid=12345 or pm_id=1


asyncio.run(pm2_manager())