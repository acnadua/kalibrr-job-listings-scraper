@echo off
REM Create virtual environment if it doesn't exist
if not exist venv (
	python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Install Playwright browsers
playwright install

REM Clear the terminal
cls

echo ===========================================================
echo              Kalibrr Job Listings Scraper
echo ===========================================================

REM Set yellow color
for /f %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"
set "YELLOW=%ESC%[33m"
set "RESET=%ESC%[0m"

REM Ask user for job position
set /p position=%YELLOW%Enter the job position you want to collect job listings for (press Enter for none): %RESET%
if "%position%"=="" set position=

REM Ask user for scroll count
set /p load=%YELLOW%How many times should the page scroll to load more job listings? (press Enter for 0): %RESET%
if "%load%"=="" set load=0

REM Run the main program with arguments
python . --position "%position%" --load %load%

pause
