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

1. Clone this repository
2. Run `python -m venv venv` to create a virtual environment and then run `./venv/Scripts/Activate.ps1` if in Windows, or `source venv/bin/activate` if running on Linux
3. Install the dependencies by running `pip install -r requirements.txt`
4. Install playwright dependencies and run `playwright install`
5. Simply run the main file using the command `python .`
6. Specify what job position to scrape by running `python . --position "<job position>"`, replace `<job_position>` with your desired role (eg. `python . --position "Data Engineer"`)
7. Specify the "pagination" or the amount of "load more" button clicks by running `python . --load <number>`, replace `<number>` with an actual integer (eg. `python . --load 5`)
8. May also combine both the `--position` and `--load` arguments like so: `python . --position "architect" --load 3`
