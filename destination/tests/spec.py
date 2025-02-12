# test_script.py
from playwright.sync_api import sync_playwright

def test_basic():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('https://blazedemo.com')
        assert "BlazeDemo" in page.title()
        page.screenshot(path='screenshot.png')
        browser.close()

test_basic()