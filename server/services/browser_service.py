from store import store
from models import BrowserConfig
from pathlib import Path
from utils.helper import write_config_file
from constant import BROWSER_PORT
from utils.commands import CamoufoxCommand
import json
import random



_browser_lunchers_dir=Path("server/launcher.config")


class BrowserService:

    async def action_create(self, identify: str | None = None):
        try:
            if identify:
                # Load existing configuration
                browser_config_json = self._get_browser_config_json_with_identify(identify)
                if not browser_config_json:
                    return {"success": False, "error": "Configuration not found"}
                browser_config = BrowserConfig(**browser_config_json)
            else:
                browser_config = BrowserConfig(port=await self._random_available_port())

            browser_command = CamoufoxCommand(browser_config)
            await browser_command.start()
            # Save configuration and store instance
            await self._save_browser_config(browser_config)
            store["browser"][browser_config.id] = browser_command

            return {
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
        return True

    async def action_delete(self,identify:str):
        return True

    async def get_info(self,identify:str):
        return True

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

    def _get_browser_config_json_with_identify(self, identify: str):
        config_path = _browser_lunchers_dir.joinpath(f"{identify}.json")
        return json.loads(config_path.read_text()) if config_path.exists() else {}