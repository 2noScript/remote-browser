import subprocess
from pm2 import PM2, AioPM2
import asyncio

pm2 = PM2()
aiopm2 = AioPM2()


port = 3010
ws_path = "browser"
headless = "false"  
geoip = "false"   
humanize = "true"


command = [
    "python", "src/launcher/init_browser.py",  
    f"--port={port}",
    f"--ws_path={ws_path}",
    f"--headless={headless}",
    f"--geoip={geoip}",
    f"--humanize={humanize}"
]


async def run_browser():

    await aiopm2.connect()

    response =await aiopm2.start({
        "script":"src/luncher/init_browser.py",
        "name":"test",
        "exec_mode": "fork",
        "interpreter": "python3",
        "args": ["--port", "5000","--ws_path","browser"]
    })



    # print("Running command:", command)
    
    # process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # stdout, stderr = process.communicate()
    
    # if stdout:
    #     print("Output:", stdout.decode())
    # if stderr:
    #     print("Error:", stderr.decode())


    # for line in process.stdout:
    #     print("Output:", line.strip())  # Đọc từng dòng stdout

    # for line in process.stderr:

    #     process.wait()
    
    # if process.returncode == 0:
    #     print("✅ Subprocess ran successfully.")
    # else:
    #     print(f"❌ Subprocess failed with return code {process.returncode}")

    # print("Subprocess finished.")
