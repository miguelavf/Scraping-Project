import json
from scraper import WebScraper
from logger import get_logger

logger = get_logger(__name__)


def main():
    """Main function to run the web scraper."""
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        logger.error("config.json not found. Please create it.")
        return

    teams = config.get("teams", {})

    if not teams:
        logger.warning("No teams found in config.json")
        return

    scraper = WebScraper()
    data = scraper.fetch_and_extract_emails(teams)

    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

    logger.info("Scraping complete. Data saved to data.json")


if __name__ == "__main__":
    main()
