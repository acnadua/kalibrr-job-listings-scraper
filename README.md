# Job Listings Web Scraper

A Python script that scrapes job listings from Kalibrr, a public job board and doesn't require logging in to access the job listings. Kalibrr is a dynamic website that requires clicking on a "load more" button to load more job listings instead of pagination. For the sake of this project, **we'll treat "pagination" as the amount of "load more" button clicks** to be made before scraping the job listings.

## Features

- JS rendering
- Headless browser
- Delay handling
- Error handling for missing fields
- Clean CSV/MongoDB output
- Idempotent data, making sure there are no duplicates, using job_url as identifier

## Sample Output

- job_url
- job_title
- company
- location
- salary_range_month
- employment_type (full_time, contractual, internship, etc.)
- work_setup (on_site, hybrid, remote)
- application_deadline
- role_rank (entry_level, mid_senior, associate_supervisor)

## Technologies Used

- Python
- Playwright
- pandas
- MongoDB

## Test Instructions:

1. Clone this repository and navigate to the generated folder using `cd kalibrr-job-listings-scraper`
2. Create a `.env` file inside the generated folder with the following variables:

```
TESTING=true #only if you want a headful browser
MONGO_URI=<your mongo connection string>
DB_NAME=<your database>
```

3. Run the script file depending on your operating system: `run.bat` if on Windows, and if on Linux, use the following commands:

```
chmod +x run.sh
./run.sh
```

4. Answer the prompts or simply press enter, and the scraper will be doing the rest.

5. The CSV files will be generated inside the repository, in a folder named `csv`. It will use the name of the job position, if you specified one. Otherwise, it will be saved into the default filename. **(Warning: It might overwrite the previous CSV files if you scraped the same position or the general job listings)**
