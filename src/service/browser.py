import subprocess

port = 8080
ws_path = "/path/to/socket"
headless = "true"  
geoip = "false"   
humanize = "true"


command = [
    "python", "run_server.py",  
    f"--port={port}",
    f"--ws_path={ws_path}",
    f"--headless={headless}",
    f"--geoip={geoip}",
    f"--humanize={humanize}"
]

process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

stdout, stderr = process.communicate()

if stdout:
    print("Output:", stdout.decode())
if stderr:
    print("Error:", stderr.decode())

process.wait()

print("Subprocess finished.")
