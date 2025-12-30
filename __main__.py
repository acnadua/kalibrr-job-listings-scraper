import argparse
from src.utils.logger import logger
from src.scraper.job_scraper import JobListingScraper

def main():
    parser = argparse.ArgumentParser(description="Job Listings Scraper")
    parser.add_argument("--position", type=str, default="", help="Job position to scrape")
    parser.add_argument("--load", type=int, default=0, help="Number of times to click the 'load more' button for more job listings")
    args = parser.parse_args()

    position = args.position
    load = args.load

    if not position:
        logger.info("Scraping job listings in Kalibrr...")
    else:
        logger.info(f"Scraping job listings for a {position} role...")

    scraper = JobListingScraper(position=position, load=load)
    scraper.start_job()
    logger.info("Scraping completed.")

if __name__ == "__main__":
    main()