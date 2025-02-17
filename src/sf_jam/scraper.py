import logging
import traceback
from typing import Dict

from database import ConcertDatabase
from models import VenueConfig

from venues.chapel import retrieve_chapel_concerts
from venues.fillmore import retrieve_fillmore_concerts
from venues.fox import retrieve_fox_concerts
from venues.warfield import retrieve_warfield_concerts
from venues.greek import retrieve_greek_concerts

logger = logging.getLogger(__name__)


class ConcertScraper:
    def __init__(self):
        self.db = ConcertDatabase()
        self.venues = {
            "The Chapel": VenueConfig(
                "The Chapel", retrieve_chapel_concerts, "The Chapel"
            ),
            "The Fillmore": VenueConfig(
                "The Fillmore", retrieve_fillmore_concerts, "The Fillmore"
            ),
            "The Warfield": VenueConfig(
                "The Warfield", retrieve_warfield_concerts, "The Warfield"
            ),
            "Fox Theatre": VenueConfig(
                "Fox Theatre", retrieve_fox_concerts, "Fox Theatre"
            ),
            "Greek Theatre": VenueConfig(
                "Greek Theatre", retrieve_greek_concerts, "Greek Theatre"
            ),
        }

    def scrape_venue(self, venue_name: str) -> bool:
        """Scrape a single venue and return success status."""
        venue_config = self.venues.get(venue_name)
        if not venue_config:
            logger.error(f"Unknown venue: {venue_name}")
            return False

        try:
            logger.info(f"Starting scrape for {venue_name}")
            concerts = venue_config.retrieval_func()

            if not concerts:
                logger.warning(f"No concerts retrieved for {venue_name}")
                return False

            inserted, errors = self.db.save_concerts(concerts, venue_config.db_name)
            success = inserted > 0 and errors == 0
            return success

        except Exception as e:
            logger.error(f"Error scraping {venue_name}: {e}\n{traceback.format_exc()}")
            return False

    def scrape_all_venues(self) -> Dict[str, bool]:
        """
        Scrape all configured venues.
        Returns dict mapping venue names to success status.
        """
        results = {}
        for venue_name in self.venues:
            results[venue_name] = self.scrape_venue(venue_name)
        return results
