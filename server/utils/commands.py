import subprocess
import json
import asyncio
import os
import re
import signal
from pathlib import Path
from threading import Event
from models import BrowserConfig



class CamoufoxCommand:
    def __init__(self, browser_config: BrowserConfig):
        self._browser_config = browser_config
        self._options = browser_config.parse()
        self._process = None
        self._ws_endpoint = None
        self._start_timeout = self._options.get("startTimeout", 30000) if self._options else 30000
        self._server_path = Path(__file__).parent.parent / "launcher/browser.py"
        self._stop_event = Event()
    async def _wait_for_server(self):
        if not self._process or not self._process.stdout:
            raise RuntimeError("Process or stdout not initialized")
        while True:
            line = await asyncio.get_event_loop().run_in_executor(None, self._process.stdout.readline)
            if not line:
                break
            # Updated regex pattern and capture the endpoint
            match = re.search(r"(ws://localhost[^\s]+)", line.strip())
            if match:
                self._ws_endpoint = match.group(1)  
                break
    async def start(self) -> str:
        if self._process:
            raise RuntimeError("Server is already running")

        config_arg = f"'{json.dumps(self._options)}'"  # Wrap the JSON string in single quotes
        command = ["python", str(self._server_path), "--config", config_arg]

        self._process = subprocess.Popen(
            command,
            cwd=str(self._server_path.parent),
            env=os.environ.copy(),
            # shell=True if os.name == "nt" else False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        try:
            await asyncio.wait_for(self._wait_for_server(), timeout=self._start_timeout / 1000)
        except asyncio.TimeoutError:
            self._cleanup()
            raise RuntimeError(f"Server start timeout after {self._start_timeout}ms")
        if self._ws_endpoint is None:
            raise RuntimeError("WebSocket endpoint not initialized")
        return self._ws_endpoint
    

    async def stop(self) -> int:
        if self._process:
            pid = self._process.pid
            try:   

                browser_cmd = f"pkill -TERM -P {pid}"
                await asyncio.create_subprocess_shell(browser_cmd)
                await asyncio.sleep(1)  # Give TERM signal time to work
                browser_cmd_force = f"pkill -KILL -P {pid}"
                await asyncio.create_subprocess_shell(browser_cmd_force)

                await asyncio.wait_for(asyncio.to_thread(self._process.wait), timeout=5)
                print("All processes terminated successfully")
            except Exception as e:
                try:
                    await asyncio.to_thread(os.kill, pid, signal.SIGKILL)
                except ProcessLookupError:
                    print("Process already terminated")
            self._cleanup()
            return 0
        return 1

    def _cleanup(self):
        self._process = None
        self._ws_endpoint = None
        self._stop_event.set()

    async def restart(self) -> str:
        await self.stop()
        return await self.start()




