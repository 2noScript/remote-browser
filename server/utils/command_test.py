import subprocess
import json
import asyncio
import os
import re
import signal
from pathlib import Path
from typing import Optional
from threading import Event

class CamoufoxServer:
    def __init__(self, options: Optional[dict] = None):
        self._process = None
        self._ws_endpoint = None
        self._start_timeout = options.get("startTimeout", 30000) if options else 30000
        self._options = {
            "headless": options.get("headless", True) if options else True,
            "geoip": options.get("geoip", True) if options else True,
            "proxy": options.get("proxy", None) if options else None,
            "humanize": options.get("humanize", True) if options else True,
            "showcursor": options.get("showcursor", True) if options else True,
            "blockImages": options.get("blockImages", False) if options else False,
            "mainWorldEval": options.get("mainWorldEval", True) if options else True,
            "debug": options.get("debug", False) if options else False,
        }
        self._server_path = Path(__file__).parent / "server.py"
        self._stop_event = Event()

    @property
    def ws_endpoint(self):
        return self._ws_endpoint

    async def start(self) -> str:
        if self._process:
            raise RuntimeError("Server is already running")

        config_arg = json.dumps(self._options).replace('"', '\\"')
        command = ["python", "-X", "utf8", str(self._server_path), "--config", config_arg]

        self._process = subprocess.Popen(
            command,
            cwd=str(self._server_path.parent),
            env=os.environ.copy(),
            shell=True if os.name == "nt" else False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        try:
            await asyncio.wait_for(self._wait_for_server(), timeout=self._start_timeout / 1000)
        except asyncio.TimeoutError:
            self._cleanup()
            raise RuntimeError(f"Server start timeout after {self._start_timeout}ms")
        return self._ws_endpoint

    async def _wait_for_server(self):
        assert self._process.stdout
        while not self._stop_event.is_set():
            line = await asyncio.get_event_loop().run_in_executor(None, self._process.stdout.readline)
            if not line:
                break
            clean_line = re.sub(r'\x1B\[[0-9;]*[mK]', '', line.strip())
            match = re.search(r'ws:\/\/[^:\s]*:[0-9]+\/[a-zA-Z0-9]+', clean_line)
            if match:
                self._ws_endpoint = match.group(0)
                break

    async def stop(self) -> int:
        if self._process:
            self._process.terminate()
            try:
                await asyncio.wait_for(asyncio.to_thread(self._process.wait), timeout=5)
            except asyncio.TimeoutError:
                os.kill(self._process.pid, signal.SIGKILL)
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
