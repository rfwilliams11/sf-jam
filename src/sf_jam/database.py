import logging
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


class ConcertDatabase:
    def __init__(self, db_path: str = "concerts.db"):
        self.db_path = db_path
        self._init_database()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def _init_database(self):
        """Initialize the database with required schema."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS concerts (
                        title TEXT,
                        date TEXT,
                        headliner TEXT,
                        venue TEXT,
                        show_time TEXT,
                        ticket_url TEXT,
                        image_url TEXT,
                        scraped_date TEXT,
                        UNIQUE(venue, date, headliner)
                    )
                """
                )
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    def save_concerts(self, concerts: List[Dict], venue: str) -> Tuple[int, int]:
        """
        Save concerts to database with error handling and duplicate prevention.
        Returns tuple of (inserted_count, error_count).
        """
        inserted = 0
        errors = 0
        current_date = datetime.now().strftime("%Y-%m-%d")

        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # Delete old records for this venue
                cursor.execute("DELETE FROM concerts WHERE venue = ?", (venue,))

                # Insert new records
                for concert in concerts:
                    try:
                        concert["scraped_date"] = current_date
                        cursor.execute(
                            """
                            INSERT INTO concerts VALUES (
                                :title, :date, :headliner, :venue,
                                :show_time, :ticket_url, :image_url, :scraped_date
                            )
                        """,
                            concert,
                        )
                        inserted += 1
                    except sqlite3.Error as e:
                        errors += 1
                        logger.error(
                            f"Error inserting concert for {venue}: {e}\nData: {concert}"
                        )

                conn.commit()
                logger.info(
                    f"Saved {inserted} concerts for {venue} (with {errors} errors)"
                )
                return inserted, errors
        except sqlite3.Error as e:
            logger.error(f"Database operation failed for {venue}: {e}")
            raise
