import argparse
from camoufox.server import launch_server

def init_browser():
    parser = argparse.ArgumentParser(description="Launch Camoufox Server")
    
    parser.add_argument('--headless', type=str, default='virtual', help='Headless mode')
    parser.add_argument('--geoip', type=bool, default=True, help='Enable GeoIP')
    parser.add_argument('--humanize', type=bool, default=True, help='Enable humanized output')
    parser.add_argument('--os', type=str, default='windows', help='Operating system')
    parser.add_argument('--webgl_config', type=str, default=("Google Inc. (NVIDIA)", "ANGLE (NVIDIA, NVIDIA GeForce GTX 980 Direct3D11 vs_5_0 ps_5_0), or similar"), help='WebGL configuration')
    parser.add_argument('--port', type=int, required=True, help='Port to run the server')
    parser.add_argument('--ws_path', type=str, required=True, help='WebSocket path')

    args = parser.parse_args()

    launch_server(
        headless=args.headless,
        geoip=args.geoip,
        humanize=args.humanize,
        os=args.os,
        webgl_config=args.webgl_config,
        port=args.port,
        ws_path=args.ws_path
    )

