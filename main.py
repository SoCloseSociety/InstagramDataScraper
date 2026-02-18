"""
Instagram Profile Scraper
by SoClose Society — https://soclose.co
Digital solutions & software development studio.

Scrapes Instagram profile links from any feed page using Selenium
browser automation. Exports unique profile URLs to CSV format.

Part of the SoClose open-source automation toolkit:
    https://github.com/soclosesociety

Usage:
    python main.py

Environment Variables:
    INSTA_USERNAME - Instagram username or email
    INSTA_PASSWORD - Instagram password

License: MIT — See LICENSE file for details.
Contact: contact@soclose.co

DISCLAIMER: This tool is provided for educational purposes only.
Scraping Instagram may violate their Terms of Service.
Use responsibly and at your own risk.
"""

import csv
import logging
import os
import random
import sys
import time
from pathlib import Path

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

MAX_STALE_ITERATIONS = 500  # Stop after this many iterations with no new links
SCROLL_PAUSE_MIN = 0.8  # Minimum pause between scrolls (seconds)
SCROLL_PAUSE_MAX = 2.0  # Maximum pause between scrolls (seconds)
SCROLL_AMOUNT = 600  # Pixels to scroll down per iteration
SAVE_INTERVAL = 50  # Save to CSV every N iterations


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------


def create_driver() -> webdriver.Chrome:
    """Create and configure a Chrome WebDriver instance."""
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver


def get_credentials() -> tuple[str, str]:
    """Retrieve Instagram credentials from environment variables or user input."""
    username = os.getenv("INSTA_USERNAME") or input("Enter Instagram username/email: ").strip()
    password = os.getenv("INSTA_PASSWORD") or input("Enter Instagram password: ").strip()

    if not username or not password:
        logger.error("Username and password are required.")
        sys.exit(1)

    return username, password


def login(driver: webdriver.Chrome, username: str, password: str) -> bool:
    """Log in to Instagram and return True on success."""
    logger.info("Navigating to Instagram login page...")
    driver.get("https://www.instagram.com/accounts/login/")

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
    except TimeoutException:
        logger.error("Login page did not load in time.")
        return False

    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    logger.info("Waiting for login to complete...")
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@id,'mount')]"))
        )
    except TimeoutException:
        logger.error("Login failed or timed out. Check your credentials.")
        return False

    logger.info("Login successful.")
    return True


EXCLUDED_PATHS = {
    "/explore/", "/accounts/", "/reels/", "/stories/", "/direct/",
    "/directory/", "/developer/", "/about/", "/legal/", "/privacy/",
    "/terms/", "/session/", "/emails/", "/settings/", "/nametag/",
}


def extract_profile_links(html: str) -> set[str]:
    """Extract Instagram profile links from page HTML source."""
    soup = BeautifulSoup(html, "lxml")
    links = set()
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        # Instagram profile links have exactly 2 slashes: /username/
        if href.count("/") == 2 and not href.startswith("http") and href not in EXCLUDED_PATHS:
            links.add(href)
    return links


def save_to_csv(links: list[str], filepath: Path) -> None:
    """Save profile links to a CSV file."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ProfileLink"])
        for link in sorted(links):
            writer.writerow([f"https://www.instagram.com{link}"])
    logger.info("Saved %d links to %s", len(links), filepath)


def scrape_profiles(driver: webdriver.Chrome, output_file: Path) -> list[str]:
    """Scroll the feed and collect unique profile links."""
    all_links: set[str] = set()
    stale_count = 0
    iteration = 0

    logger.info("Starting scrape — scroll the page or let the script run.")
    logger.info("Press Ctrl+C to stop early and save results.\n")

    try:
        while stale_count < MAX_STALE_ITERATIONS:
            iteration += 1
            prev_count = len(all_links)

            html = driver.page_source
            new_links = extract_profile_links(html)
            all_links.update(new_links)

            current_count = len(all_links)

            if current_count == prev_count:
                stale_count += 1
            else:
                stale_count = 0

            if iteration % 10 == 0:
                logger.info(
                    "Iteration %d | Links found: %d | Stale: %d/%d",
                    iteration,
                    current_count,
                    stale_count,
                    MAX_STALE_ITERATIONS,
                )

            # Periodic save
            if iteration % SAVE_INTERVAL == 0:
                save_to_csv(list(all_links), output_file)

            # Scroll down with randomized delay to appear more human
            driver.execute_script(f"window.scrollBy(0, {SCROLL_AMOUNT});")
            time.sleep(random.uniform(SCROLL_PAUSE_MIN, SCROLL_PAUSE_MAX))

    except KeyboardInterrupt:
        logger.info("\nScraping interrupted by user.")

    return sorted(all_links)


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------


def main() -> None:
    """Main entry point for the Instagram Profile Scraper."""
    logger.info("Instagram Profile Scraper — by SoClose Society (soclose.co)")
    logger.info("=" * 50)

    username, password = get_credentials()
    output_name = input("Enter output file name (without extension): ").strip() or "instagram_profiles"
    output_file = Path(f"{output_name}.csv")

    driver = create_driver()

    try:
        if not login(driver, username, password):
            logger.error("Could not log in. Exiting.")
            return

        input("\nNavigate to the page you want to scrape, then press ENTER to start...")

        links = scrape_profiles(driver, output_file)
        save_to_csv(links, output_file)

        logger.info("=" * 50)
        logger.info("Scraping complete! %d unique profiles saved to %s", len(links), output_file)

    except WebDriverException as e:
        logger.error("Browser error: %s", e)
    finally:
        driver.quit()
        logger.info("Browser closed.")


if __name__ == "__main__":
    main()
