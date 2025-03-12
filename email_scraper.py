import requests
from bs4 import BeautifulSoup
import requests.exceptions
from urllib.parse import urlsplit, urljoin
from collections import deque
import re
import argparse
import logging
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Hacker-themed ASCII art
HACKER_ART = f"""
{Fore.GREEN}
    _   _            _      _____ _           _             
 | | | | __ _  ___| | __ |_   _| |__   __ _| | _____ _ __ 
 | |_| |/ _` |/ __| |/ /   | | | '_ \ / _` | |/ / _ \ '__|
 |  _  | (_| | (__|   <    | | | | | | (_| |   <  __/ |   
 |_| |_|\__,_|\___|_|\_\   |_| |_| |_|\__,_|_|\_\___|_|   
                  Email Scraper - Professional Hacker Edition   
{Style.RESET_ALL}
"""

def print_banner():
    """Print the hacker-themed banner."""
    print(HACKER_ART)
    print(f"{Fore.CYAN}[+] Web Scraper for Emails - Professional Hacker Edition{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[+] Author: Shiboshree Roy{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[+] Version: 0.0.1{Style.RESET_ALL}")
    print(f"{Fore.RED}[+] Use responsibly!{Style.RESET_ALL}\n")

def scrape_emails(url, max_urls=100):
    """
    Scrape emails from the given URL and its linked pages.
    
    :param url: The starting URL to scrape.
    :param max_urls: Maximum number of URLs to process.
    :return: A set of unique emails found.
    """
    urls_to_process = deque([url])
    scraped_urls = set()
    emails = set()
    count = 0

    try:
        while urls_to_process and count < max_urls:
            count += 1
            current_url = urls_to_process.popleft()
            scraped_urls.add(current_url)

            logger.info(f"{Fore.BLUE}[{count}] Processing: {Fore.WHITE}{current_url}{Style.RESET_ALL}")

            try:
                response = requests.get(current_url, timeout=10)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                logger.warning(f"{Fore.YELLOW}Skipping {current_url} due to error: {e}{Style.RESET_ALL}")
                continue

            # Extract emails
            new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
            emails.update(new_emails)

            # Parse the page for links
            soup = BeautifulSoup(response.text, 'html.parser')
            for anchor in soup.find_all("a", href=True):
                link = anchor["href"]
                full_link = urljoin(current_url, link)
                if full_link not in scraped_urls and full_link not in urls_to_process:
                    urls_to_process.append(full_link)

            logger.info(f"{Fore.GREEN}Total emails found so far: {Fore.WHITE}{len(emails)}{Style.RESET_ALL}")

    except KeyboardInterrupt:
        logger.info(f"{Fore.RED}[-] Exiting program due to user interrupt.{Style.RESET_ALL}")
    except Exception as e:
        logger.error(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

    return emails

def save_emails_to_file(emails, filename="emails.txt"):
    """
    Save the scraped emails to a file.
    
    :param emails: A set of emails to save.
    :param filename: The name of the file to save the emails to.
    """
    with open(filename, "w") as file:
        for email in emails:
            file.write(email + "\n")
    logger.info(f"{Fore.GREEN}Saved {Fore.WHITE}{len(emails)}{Fore.GREEN} emails to {Fore.WHITE}{filename}{Style.RESET_ALL}")

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Web Scraper for Emails - Professional Hacker Edition")
    parser.add_argument("url", help="The target URL to start scraping from")
    parser.add_argument("-m", "--max-urls", type=int, default=100, help="Maximum number of URLs to process (default: 100)")
    parser.add_argument("-o", "--output", default="emails.txt", help="Output file to save emails (default: emails.txt)")
    args = parser.parse_args()

    logger.info(f"{Fore.CYAN}Starting scraping from: {Fore.WHITE}{args.url}{Style.RESET_ALL}")
    emails = scrape_emails(args.url, args.max_urls)
    save_emails_to_file(emails, args.output)

if __name__ == "__main__":
    main()