#!/usr/bin/env python3

import os
import sys
import signal
import multiprocessing
from camoufox.server import launch_server
from fastapi import FastAPI
import uvicorn
import threading


def launch_server_instance(name, port, ws_path):
    try:
        server = launch_server(
            headless="virtual",
            geoip=True,
            humanize=True,
            os='windows',
            webgl_config=("Google Inc. (NVIDIA)", "ANGLE (NVIDIA, NVIDIA GeForce GTX 980 Direct3D11 vs_5_0 ps_5_0), or similar"),
            port=port,
            ws_path=ws_path
        )
        print(f"Server {name} đã khởi chạy:", server)
    except Exception as e:
        print(f"Error while launching server {name}: {e}")

# Launch two servers in parallel
thread1 = threading.Thread(target=launch_server_instance, args=('server1', 3002, 'browser'))
# thread2 = threading.Thread(target=launch_server_instance, args=('server2', 3002, 'browser1'))

thread1.start()
# thread2.start()

# Wait for both threads to complete
thread1.join()
# thread2.join()