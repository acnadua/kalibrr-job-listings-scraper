from pymongo import MongoClient, UpdateOne
from datetime import datetime, timezone
from src.models.job_listing import JobListing
from src.utils.constants import MONGO_URI, DB_NAME
from src.utils.logger import logger

class MongoDBClient:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client.get_database(DB_NAME)

    def save_job_listings(self, job_listings: list[JobListing] | None):
        if not job_listings:
            return
        
        collection = self.db.get_collection("kalibrr_job_listings")
        
        try:
            updates = []
            current_date = datetime.now(timezone.utc)
            for job in job_listings:
                payload = job.model_dump()
                date_created = payload.pop("date_created", current_date)
                updates.append(UpdateOne(
                    {"job_url": payload["job_url"]},
                    {
                        "$set": payload,
                        "$setOnInsert": {"date_created": date_created}
                    },
                    upsert=True
                ))

            if updates:
                result = collection.bulk_write(updates)
                logger.debug(f"Upserted {result.upserted_count} and modified {result.modified_count} job listings.")
        except Exception as e:
            logger.error(f"Error storing job listings in database: {e}")