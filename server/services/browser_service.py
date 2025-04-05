from re import T
from store import store
from models import BrowserConfig
from pathlib import Path
from utils.helper import write_config_file
from constant import BROWSER_PORT
from utils.commands import CamoufoxCommand
from playwright.async_api import async_playwright
import json
import random



_browser_lunchers_dir=Path("server/launcher.config")


class BrowserService:

    async def action_create(self, identify: str | None = None):
        try:
            if identify:
                browser_config_json = self._get_browser_config_json_with_identify(identify)
                if not browser_config_json:
                    return {"success": False, "error": "Configuration not found"}
                browser_config = BrowserConfig(
                    id=browser_config_json["id"], 
                    port=browser_config_json["port"],
                    config=browser_config_json["config"])
            else:
                browser_config = BrowserConfig(
                    port=await self._random_available_port())

            browser_command = CamoufoxCommand(browser_config)
            await browser_command.start()
            await self._save_browser_config(browser_config)
            store["browser"][self._get_identify(browser_config)] = browser_command

            return {
                "pid": browser_command.get_pid(),
                "success": True,
                "browser_id": browser_config.id,
                "port": browser_config.port
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def action_start(self,identify:str):    
        return await self.action_create(identify=identify)

        
    async def action_stop(self,identify:str):
        browser_command=store["browser"].get(identify)
        if not browser_command:
            return True
        await browser_command.stop()
        return True

    async def action_delete(self,identify:str):
        await self.action_stop(identify)
        await self._delete_browser_config_json(identify)
        return True

    async def get_info(self,identify:str):
        return await self._check_info_browser(identify)

    async def get_list(self):
        return await self._load_info_browser_config_list()

    async def _save_browser_config(self,browser_config:BrowserConfig):
        await write_config_file(
            path=_browser_lunchers_dir,
            name=self._get_identify(browser_config),
            content=json.dumps(browser_config.parse()))

    async def _load_info_browser_config_list(self):
        return [json.loads(cfg.read_text()) for cfg in _browser_lunchers_dir.glob("*.json")]

    async def _check_port_has_used(self,port:int):
        browser_config_list=await self._load_info_browser_config_list()
        for cfg in browser_config_list:
            if cfg["port"]==port:
                return True
        return False
    
    async def _random_available_port(self):
        while True:
            port=random.randint(BROWSER_PORT[0],BROWSER_PORT[1])
            if not await self._check_port_has_used(port):
                return port

    def _get_identify(self,browser_config:BrowserConfig):
        return f"{browser_config.id}_{browser_config.port}"

    async def _delete_browser_config_json(self, identify: str) -> bool:
        try:
            config_path = _browser_lunchers_dir.joinpath(f"{identify}.json")
            if config_path.exists():
                config_path.unlink()
                return True
            return False
        except Exception:
            return False

    def _get_browser_config_json_with_identify(self, identify: str) -> dict:
        try:
            config_path = _browser_lunchers_dir.joinpath(f"{identify}.json")
            if not config_path.exists():
                return {}
            
            id, port = identify.split('_')
            config_data = json.loads(config_path.read_text())
            
            return {
                "config": config_data,
                "id": id,
                "port": int(port)  # Convert port to integer
            }
        except (json.JSONDecodeError, ValueError, IndexError):
            return {}
    
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
                "connected": True,
                "url": connect_url,
                "context_count": context_count,
                "context_info": context_info
            }



