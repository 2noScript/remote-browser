from re import T
from store import store
from pathlib import Path
from constant import BROWSER_PORT
from lib.commands import CamoufoxCommand
from playwright.async_api import async_playwright
import random
from db import BrowserDB
import uuid


_browser_lunchers_dir=Path("server/launcher.config")

class BrowserService:

    async def action_create(self):
        try:
            port=await self._random_available_port()
            ws_path = str(uuid.uuid4())[:8]

            browser=await BrowserDB.create(
                identify=f"{ws_path}_{port}",
                config={
                    "port": port,
                    "ws_path": ws_path
                })

            return {
                "id": browser.id,
                "success": True,
                "identify": browser.identify,
                "config": browser.config,
                "is_running": browser.is_running
            }
     
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def action_start(self,identify:str):
        if store["browser"].get(identify):
            return {
                "success": True,
                "message": "Browser instance already running with this identifier",
                "pid_id": store["browser"][identify].get_pid()
            }

        browser_db = await BrowserDB.get(identify)
        browser_command=CamoufoxCommand(browser_db)
        await browser_command.start()
        await  BrowserDB.update(browser_db.identify,config=browser_db.config,is_running=True)
        store["browser"][identify]=browser_command
        return {
            "success": True,
            "pid_id": browser_command.get_pid(),
            "message": "Browser instance started successfully"
        }

    async def action_stop(self,identify:str):
        browser_command=store["browser"].get(identify)
        if not browser_command:
            return {
                "success": True,
                "message": "Browser instance not running"
            }
        await browser_command.stop()
        store["browser"].pop(identify)
        await  BrowserDB.update(identify=identify,is_running=False)
        return {
            "success": True,
            "message": "Browser instance stopped successfully"
        }

    async def action_delete(self,identify:str):
        await self.action_stop(identify)
        await BrowserDB.delete(identify)
        return True

    async def get_info(self,identify:str):
        print(identify)
        return await BrowserDB.get(identify)

    async def get_list(self):
        return await BrowserDB.get_all()

    async def _check_port_has_used(self, port: int):
        all_browser_db = await BrowserDB.get_all()
        for browser_db in all_browser_db:
            if browser_db.config.get("port") == port:
                return True
        return False
    
    async def _random_available_port(self):
        while True:
            port=random.randint(BROWSER_PORT[0],BROWSER_PORT[1])
            if not await self._check_port_has_used(port):
                return port

 

    
    async def _check_info_browser(self, identify: str):
        id, port = identify.split('_')
        connect_url = f"ws://localhost:{port}/{id}"
        async with async_playwright() as p:
            browser = await p.firefox.connect(connect_url)
            context= await browser.new_context()
            page=await context.new_page()
            await page.goto("https://example.com")

            context_count = len(browser.contexts)
            context_info=[]
            for context in browser.contexts:
                
                page_info=[]
                for page in context.pages:
                    page_info.append({
                        "url": page.url,
                        "title": await page.title(),
                        "client": {
                            "ip": await page.evaluate("() => fetch('https://api.ipify.org?format=json').then(r => r.json())"),
                            "user_agent": await page.evaluate("() => navigator.userAgent")
                        }
                    })
                context_info.append({
                    "page_count":len(context.pages),
                    "page_info":page_info
                })


 
            await browser.close()
            return {
                "success": True,
            }



