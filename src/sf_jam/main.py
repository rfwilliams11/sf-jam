import logging
import traceback
from datetime import datetime
import time
import schedule
import threading
from scraper import ConcertScraper

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("concert_scraper.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


def scrape_task():
    try:
        scraper = ConcertScraper()
        results = scraper.scrape_all_venues()

        # Log overall results
        success_count = sum(1 for success in results.values() if success)
        logger.info(
            f"Scraping completed at {datetime.now()}. {success_count}/{len(results)} venues successful"
        )

        for venue, success in results.items():
            status = "✓" if success else "✗"
            logger.info(f"{status} {venue}")

    except Exception as e:
        logger.error(f"Critical error in scrape_task: {e}\n{traceback.format_exc()}")


def main():
    try:
        # Run initial scrape
        logger.info("Starting initial scrape...")
        scrape_task()

        # Schedule daily scrape
        schedule.every().day.at("05:00").do(scrape_task)  # Runs at midnight

        # Create and start scheduler thread
        scheduler_thread = threading.Thread(target=run_scheduler)
        scheduler_thread.daemon = True  # Thread will exit when main program exits
        scheduler_thread.start()

        # Keep main thread alive
        while True:
            time.sleep(1)

    except Exception as e:
        logger.error(f"Critical error in main: {e}\n{traceback.format_exc()}")
        raise


if __name__ == "__main__":
    main()
