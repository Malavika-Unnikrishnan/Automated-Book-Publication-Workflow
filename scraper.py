# scraper.py

import sys
import asyncio


if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())




from playwright.sync_api import sync_playwright
import os

def get_chapter_text_and_image(url: str, save_dir: str = "data/raw"):
    os.makedirs(save_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        
        page.wait_for_selector("#mw-content-text")

        # Get chapter title
        title = page.title().replace(" ", "_").replace("/", "_")

        # Get text content
        content = page.query_selector("#mw-content-text").inner_text()

        # Save screenshot
        screenshot_path = os.path.join(save_dir, f"{title}.png")
        page.screenshot(path=screenshot_path, full_page=True)

        # Save text
        text_path = os.path.join(save_dir, f"{title}.txt")
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(content)

        browser.close()

    return content, title, screenshot_path
