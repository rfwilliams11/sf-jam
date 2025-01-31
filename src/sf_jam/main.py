import sqlite3
from datetime import datetime
from chapel import retrieve_chapel_concerts
from fillmore import retrieve_fillmore_concerts
from warfield import retrieve_warfield_concerts
from fox import retrieve_fox_concerts


def init_database():
    """Create SQLite database and concerts table if not exists."""
    conn = sqlite3.connect("concerts.db")
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
            scraped_date TEXT
        )
    """
    )
    conn.commit()
    return conn, cursor


def save_concerts_to_db(concerts, venue, conn, cursor):
    """Delete existing venue records and insert new concerts."""
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Delete existing records for this venue
    cursor.execute("DELETE FROM concerts WHERE venue = ?", (venue,))

    # Insert new records with scrape date
    for concert in concerts:
        concert["scraped_date"] = current_date

    cursor.executemany(
        """
        INSERT INTO concerts VALUES (
            :title, :date, :headliner, :venue, 
            :show_time, :ticket_url, :image_url, :scraped_date
        )
    """,
        concerts,
    )

    conn.commit()
    print(f"Refreshed {len(concerts)} concerts for {venue}")


def main():
    venues = {
        1: ("The Chapel", retrieve_chapel_concerts, "The Chapel"),
        2: ("The Fillmore", retrieve_fillmore_concerts, "The Fillmore"),
        3: ("The Warfield", retrieve_warfield_concerts, "The Warfield"),
        4: ("Fox Theatre", retrieve_fox_concerts, "Fox Theatre"),
    }

    conn, cursor = init_database()

    for key, (name, retrieval_func, venue_name) in venues.items():
        concerts = retrieval_func()
        save_concerts_to_db(concerts, venue_name, conn, cursor)

    conn.close()


if __name__ == "__main__":
    main()
