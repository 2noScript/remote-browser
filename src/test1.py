from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Example endpoint
    browser = p.firefox.connect('ws://localhost:5000/3002')
    page = browser.new_page()