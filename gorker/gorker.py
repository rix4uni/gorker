import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import argparse

# ANSI color codes
REDCOLOR = '\033[91m'
GREENCOLOR = '\033[92m'
CYANCOLOR = '\033[96m'
RESETCOLOR = '\033[0m'

# prints the version message
version = "v0.0.1"

def PrintVersion():
    print(f"Current gorker version {version}")

def PrintBanner():
    banner = rf"""
                            __              
       ____ _ ____   _____ / /__ ___   _____
      / __ `// __ \ / ___// //_// _ \ / ___/
     / /_/ // /_/ // /   / ,<  /  __// /    
     \__, / \____//_/   /_/|_| \___//_/     
    /____/"""
    print(f"{banner}\n\t\tCurrent gorker version {version}\n")

# Argument parser setup
parser = argparse.ArgumentParser(description="Google dorking with Selenium")
parser.add_argument('--gui', action='store_true', help='Run in gui mode')
parser.add_argument('--wait', type=int, default=20, help='reCAPTCHA wait time in seconds (default 20)')
parser.add_argument('-o', '--output', help='Output file to save results')
parser.add_argument('--silent', action='store_true', help='Run without printing the banner')
parser.add_argument('--version', action='store_true', help='Show current version of gorker')
parser.add_argument('--verbose', action='store_true', help='Enable verbose mode')
args = parser.parse_args()

if args.version:
    PrintBanner()
    PrintVersion()
    exit(1)

if not args.silent:
    PrintBanner()

def handle_recaptcha():
    """Check for reCAPTCHA and wait for manual solving."""
    if "google.com/sorry/index?continue=" in driver.current_url:
        print(f"{CYANCOLOR}reCAPTCHA found. Please solve manually. Waiting 20 seconds... {driver.current_url}{RESETCOLOR}")
        time.sleep(args.wait)
    else:
        print(f"{CYANCOLOR}No reCAPTCHA detected. Continuing... {driver.current_url}{RESETCOLOR}")

def save_output():
    if args.output:
        with open(args.output, 'a') as file:
            file.write(f"{link} [{title}]\n")

# Set up Chrome options
options = webdriver.ChromeOptions()
if not args.gui:
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(options=options)

def main():
    try:
        # Read URLs from standard input
        for url in sys.stdin:
            url = url.strip()  # Remove any whitespace or newline characters
            if not url:
                continue  # Skip empty lines

            # Check if URL starts with http:// or https://
            if not (url.startswith("http://") or url.startswith("https://")):
                print(f"Skipped invalid URL: {url}")
                continue

            # Start with the first page (num=100)
            current_url = url + "&num=100&start=0"

            # Loop through the results based on the count
            try:
                # Navigate to the initial URL
                driver.get(current_url)
                print(f"{GREENCOLOR}Scraping results for: {current_url}{RESETCOLOR}")
                handle_recaptcha()

                # Parse the page source using BeautifulSoup
                soup = BeautifulSoup(driver.page_source, "html.parser")

                # Find all elements with the class 'yuRUbf'
                results = soup.find_all("div", class_="yuRUbf")

                for result in results:
                    # Extract the URL and Title
                    link_tag = result.find("a", jsname="UWckNb")
                    title_tag = result.find("h3")

                    link = link_tag["href"] if link_tag else None
                    title = title_tag.text if title_tag else "[]"

                    if link:
                        print(f"{link} [{title}]")
                        save_output()

                # Find all <td> with class "NKTSme"
                td_elements = soup.find_all('td', class_='NKTSme')

                # Count the number of <a> tags inside <td> elements
                count = sum(1 for td in td_elements if td.find('a'))  # Increment count if <a> exists

                # Check if count is greater than 0
                if count > 0:
                    print(f"{REDCOLOR}Checking total pages found: {count}{RESETCOLOR}")
                    for start in range(100, count * 100 + 1, 100):
                        next_url = f"{url}&num=100&start={start}"
                        print(f"{GREENCOLOR}Scraping results for: {next_url}{RESETCOLOR}")
                        driver.get(next_url)
                        handle_recaptcha()

                        soup = BeautifulSoup(driver.page_source, "html.parser")
                        
                        # Process the next page
                        results = soup.find_all("div", class_="yuRUbf")
                        for result in results:
                            link_tag = result.find("a", jsname="UWckNb")
                            title_tag = result.find("h3")
                            link = link_tag["href"] if link_tag else None
                            title = title_tag.text if title_tag else "[]"
                            if link:
                                print(f"{link} [{title}]")
                                save_output()
                else:
                    # Handle case where count is 0
                    if args.verbose:
                        print(f"{REDCOLOR}No additional pages found.{RESETCOLOR}")



                # Check if elements with class="card-section" exist
                card_sections = soup.find_all(class_="card-section")
                if card_sections:  # If the list is not empty, the class exists
                    if args.verbose:
                        print(f"{REDCOLOR}Checking: card-section class exist{RESETCOLOR}")

                    # Check class 'card-section' is exist or not, run this code if exist
                    current_url = url + "&num=100&start=0&filter=0"

                    # Navigate to the initial URL
                    driver.get(current_url)
                    handle_recaptcha()

                    # Parse the page source using BeautifulSoup
                    soup = BeautifulSoup(driver.page_source, "html.parser")

                    # Find all elements with the class 'yuRUbf'
                    results = soup.find_all("div", class_="yuRUbf")

                    for result in results:
                        # Extract the URL and Title
                        link_tag = result.find("a", jsname="UWckNb")
                        title_tag = result.find("h3")

                        link = link_tag["href"] if link_tag else None
                        title = title_tag.text if title_tag else "[]"

                        if link:
                            print(f"{link} [{title}]")
                            save_output()

                    # Find all <td> with class "NKTSme"
                    td_elements = soup.find_all('td', class_='NKTSme')

                    # Count the number of <a> tags inside <td> elements
                    count = sum(1 for td in td_elements if td.find('a'))  # Increment count if <a> exists

                    # Check if count is greater than 0 for filter=0
                    if count > 0:
                        print(f"{REDCOLOR}Checking total pages found for filter=0: {count}{RESETCOLOR}")
                        for start in range(100, count * 100 + 1, 100):  # Fix here: +1 to include the last page
                            next_url = f"{url}&num=100&start={start}&filter=0"
                            print(f"{GREENCOLOR}Scraping results for: {next_url}{RESETCOLOR}")
                            driver.get(next_url)
                            handle_recaptcha()

                            soup = BeautifulSoup(driver.page_source, "html.parser")
                            
                            # Process the next page of results (similar to the first)
                            results = soup.find_all("div", class_="yuRUbf")
                            for result in results:
                                link_tag = result.find("a", jsname="UWckNb")
                                title_tag = result.find("h3")
                                link = link_tag["href"] if link_tag else None
                                title = title_tag.text if title_tag else "[]"
                                if link:
                                    print(f"{link} [{title}]")
                                    save_output()
                    else:
                        # Handle case where count is 0
                        if args.verbose:
                            print(f"{REDCOLOR}No additional pages found. for filter=0{RESETCOLOR}")
                else:
                    if args.verbose:
                        print(f"{REDCOLOR}'card-section' class not found. Skipping{RESETCOLOR}")

            except TimeoutException:
                print(f"Timeout while loading URL: {url}")

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()