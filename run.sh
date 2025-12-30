#!/bin/bash
# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
	python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Clear the terminal
clear

echo "==========================================================="
echo "             Kalibrr Job Listings Scraper"
echo "==========================================================="

# Set yellow color
YELLOW='\033[1;33m'
RESET='\033[0m'

# Prompt user for job position
read -e -p "$(echo -e ${YELLOW}Enter the job position you want to collect job listings for (press Enter for none): ${RESET})" position
if [ -z "$position" ]; then
	position=""
fi

# Prompt user for scroll count
read -e -p "$(echo -e ${YELLOW}How many times should the page scroll to load more job listings? (press Enter for 0): ${RESET})" load
if [ -z "$load" ]; then
	load=0
fi

# Run the main program with arguments
python . --position "$position" --load $load
