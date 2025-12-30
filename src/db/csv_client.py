import pandas as pd
from src.models.job_listing import JobListing
from src.utils.logger import logger

class CSVClient:
    def save_to_csv(
        self, job_listings: list[JobListing] | None, 
        file_path: str
    ):
        if not job_listings:
            return
        
        try:
            df = pd.DataFrame([job.model_dump() for job in job_listings])
            df.to_csv(file_path, index=False)
            logger.debug(f"Saved {len(job_listings)} job listings to {file_path}.")
        except Exception as e:
            logger.error(f"Error saving job listings to CSV: {e}")