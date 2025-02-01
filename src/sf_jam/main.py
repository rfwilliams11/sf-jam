import logging
import traceback
from scraper import ConcertScraper

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("concert_scraper.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main():
    try:
        scraper = ConcertScraper()
        results = scraper.scrape_all_venues()

        # Log overall results
        success_count = sum(1 for success in results.values() if success)
        logger.info(
            f"Scraping completed. {success_count}/{len(results)} venues successful"
        )

        for venue, success in results.items():
            status = "✓" if success else "✗"
            logger.info(f"{status} {venue}")

    except Exception as e:
        logger.error(f"Critical error in main: {e}\n{traceback.format_exc()}")
        raise


if __name__ == "__main__":
    main()
