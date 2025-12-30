import time, random
from datetime import datetime, timezone, timedelta
from playwright.sync_api import Page, ElementHandle
from src.db.csv_client import CSVClient
from src.db.mongo_client import MongoDBClient
from src.scraper.human_behavior import HumanBehaviorSimulator
from src.scraper.browser import setup_browser
from src.scraper.selectors import JOBS
from src.utils.constants import BASE_URL
from src.models.job_listing import JobListing
from src.utils.logger import logger

class JobListingScraper:
    def __init__(self, position: str = "", load: int = 0):
        self.mongo_client = MongoDBClient()
        self.csv_client = CSVClient()
        self.position = position
        self.load = load
        self.human_simulator = HumanBehaviorSimulator()

    def start_job(self):
        with setup_browser() as page:
            page.goto(
                self._get_search_url(), 
                wait_until="domcontentloaded", 
                timeout=60000
            )

            time.sleep(random.uniform(2, 4))  # Simulate scraping delay
            self._load_job_listings(page)
            logger.info("Finished loading job listings. Getting job data...")
            jobs = self._scrape(page)

            # !! You may comment out one of the saving methods if not needed
            logger.info("Saving job listings to MongoDB...")
            self.mongo_client.save_job_listings(jobs)

            logger.info("Saving job listings to CSV...")
            filename = "csv/job_listings.csv"
            if self.position:
                filename = f"csv/{self.position.replace(' ', '_').lower()}.csv"
            self.csv_client.save_to_csv(jobs, file_path=filename)

    def _scrape(self, page: Page):
        job_list = page.query_selector(JOBS)
        if not job_list:
            logger.warning("No job listings found on the page.")
            return
        
        jobs = job_list.query_selector_all("> div")
        logger.debug(f"Found {len(jobs)} job listings.")

        collected_jobs = []
        for job in jobs:
            try:
                job_details = self._extract_job_details(job)
                if not job_details:
                    continue
                collected_jobs.append(JobListing(**job_details))
            except Exception as e:
                logger.error(f"Error extracting job details: {e}")
                continue
            
        logger.info(f"Collected {len(collected_jobs)} job listings.")
        return collected_jobs
            
    def _extract_job_details(self, job: ElementHandle) -> dict:
        title = job.query_selector("h2 > a")
        if not title:
            return {}
        
        href = title.get_attribute("href")
        job_url = f"{BASE_URL}{href}"
        job_title = title.text_content()

        company_element = job.query_selector("h2 ~ span > a")
        if not company_element:
            company_element = job.query_selector("> div > div > span > a")
        company = company_element.text_content() if company_element else ""

        info_container = job.query_selector_all("> div.k-relative > div")
        if not info_container or len(info_container) < 3:
            return {}
        
        job_details = info_container[0].query_selector_all("> span")
        if len(job_details) < 4:
            return {}
        
        location = job_details[0].text_content()

        salary = job_details[1].text_content()
        salary_range_month = salary.replace("/ month", "").strip() if salary else ""

        employment = job_details[2].query_selector("> span")
        employment_type = employment.text_content() if employment else ""

        if len(job_details) < 5:
            work_setup = self._get_work_setup()
        else:
            setup = job_details[4].query_selector("> div > span")
            work = setup.text_content() if setup else ""
            work_setup = self._get_work_setup(work)

        more_details = info_container[1].query_selector_all("> span")
        if len(more_details) < 2:
            return {}
        
        # setup application deadline
        deadline = more_details[0].text_content()
        deadline = deadline.replace("Apply before", "").strip() if deadline else ""
        current_year = datetime.now().year
        date = datetime.strptime(f"{deadline} {current_year}", "%d %b %Y")
        date = date.replace(tzinfo=timezone(timedelta(hours=8)))  # Set to UTC+8
        application_deadline = date.astimezone(timezone.utc)

        role_rank = more_details[1].text_content()

        return {
            "job_url": job_url,
            "job_title": job_title,
            "company": company,
            "location": location,
            "salary_range_month": salary_range_month,
            "employment_type": employment_type,
            "work_setup": work_setup,
            "application_deadline_utc": application_deadline,
            "role_rank": role_rank,
        }
    
    def _get_work_setup(self, work_setup: str | None = None):
        if work_setup in ["Remote", "Hybrid"]:
            return work_setup
        
        return "On-site"

    def _load_job_listings(self, page: Page):
        for _ in range(self.load):
          self.human_simulator.scroll_until_end(page)
          time.sleep(random.uniform(2, 4)) # Simulate user reading time
          success = self.human_simulator.click_load_more(page)

          if not success:
              logger.warning("No more 'load more' button found or unable to click it.")
              break
        
        self.human_simulator.scroll_until_end(page) # final scroll to load all jobs

    def _get_search_url(self) -> str:
        search_url = f"{BASE_URL}/home"
        if self.position:
            return f"{search_url}/te/{self.position.replace(' ', '-').lower()}"
        return search_url