import time, random
from playwright.sync_api import Page
from src.scraper.selectors import LOAD_BTN
from src.utils.logger import logger

class HumanBehaviorSimulator:
    def scroll_until_end(self, page: Page):
        logger.debug("Scrolling down...")
        total_height = page.evaluate('document.body.scrollHeight')
        current_position = 0
        
        while current_position < total_height:
            scroll_distance = random.randint(300, 800)
            page.evaluate(f'window.scrollBy({{top: {scroll_distance}, behavior: "smooth"}})')
            current_position += scroll_distance
            
            time.sleep(random.uniform(0.5, 2))
            
            if random.random() < 0.1:
                scroll_back = random.randint(50, 150)
                page.evaluate(f'window.scrollBy({{top: -{scroll_back}, behavior: "smooth"}})')
                time.sleep(random.uniform(0.3, 0.8))
            
            if random.random() < 0.15:
                time.sleep(random.uniform(2, 4))
            
            total_height = page.evaluate('document.body.scrollHeight')

    def click_load_more(self, page: Page):
        logger.debug("Clicking the 'load more' button...")
        load_btn = page.query_selector(LOAD_BTN)

        if load_btn:
            load_btn.click()
            time.sleep(random.uniform(1, 3))  # Wait for new content to load
            logger.debug("'Load more' button clicked.")
            return True
        
        return False