from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.firefox.connect('ws://localhost:8080/3002')
    page = browser.new_page()
    page.goto('https://example.com')  # Change this to the URL of your choice
    title = page.title()
    print(f"Page title: {title}")
