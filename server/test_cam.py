from camoufox.sync_api import Camoufox
import time 

with Camoufox(
    config={
        # 'webrtc:ipv4': '123.45.67.89',
        'webrtc:ipv6': 'e791:d37a:88f6:48d1:2cad:2667:4582:1d6d',
    }
) as browser:
    page = browser.new_page()
    # page.goto("https://www.browserscan.net/webrtc")
    page.goto("https://test-ipv6.com/")
    time.sleep(1000)
