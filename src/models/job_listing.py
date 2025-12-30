from pydantic import BaseModel, Field
from datetime import datetime, timezone

class JobListing(BaseModel):
    job_url: str
    job_title: str
    company: str
    location: str
    salary_range_month: str
    employment_type: str
    work_setup: str | None
    application_deadline_utc: datetime
    role_rank: str
    date_created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    date_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))