from contextlib import contextmanager
from playwright.sync_api import sync_playwright
from src.utils.constants import TESTING
from src.utils.logger import logger

@contextmanager
def setup_browser():
    # Code to initialize and configure the browser
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not TESTING)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="en-US",
            timezone_id="Asia/Singapore",  # UTC+8
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            }
        )

        page = context.new_page()
        try:
            yield page
        except Exception as e:
            logger.error(f"An error occurred while using the browser: {e}")
            raise
        finally:
            if page:
                page.close()

            if context:
                context.close()

            if browser:
              browser.close()