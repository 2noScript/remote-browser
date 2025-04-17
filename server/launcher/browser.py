import sys
import json
import argparse
from camoufox.server import launch_server
from browserforge.fingerprints import Screen

class BrowserLauncher:
    def __init__(self):
        # Set UTF-8 encoding for console output
        if sys.platform == 'win32':
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

    def _parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--config', type=str,
                            help='JSON configuration')
        return parser.parse_args()

    def _load_config(self):
        args = self._parse_arguments()
        try:
            if args.config:
                config_str = args.config.strip().strip('"\'')
                return json.loads(config_str)
            return {}
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON configuration: {e}")
            print(f"Received config string: {args.config}")
            return {}

    def launch(self):
        config = self._load_config()
        launch_options ={
            "ws_path":"browser",
            "os":["windows", "macos", "linux"],
            "screen":Screen(max_width=1920, max_height=1080),
            "humanize":True,
            "headless":"virtual",
            "geoip":True,
            **config,

        }
        launch_server(**launch_options)



# python server/launcher/browser.py --config '{"headless": false, "debug": true}'
if __name__ == "__main__":
    launcher = BrowserLauncher()
    launcher.launch()