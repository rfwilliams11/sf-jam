from typing import List

import requests
from bs4 import BeautifulSoup
from models import Concert
from util import parse_concert_date


def retrieve_chapel_concerts() -> List[Concert]:
    """
    Retrieve concert listings from The Chapel website

    Returns:
        (List[Concert]): List of Concert objects
    """
    concerts = []

    for i in range(1, 4):
        url = f"https://www.thechapelsf.com/music/?list1page={i}"
        page_concerts = fetch_and_parse_concerts(url)
        concerts.extend(page_concerts)

    return concerts


def fetch_and_parse_concerts(url: str) -> List[Concert]:
    """
    Fetch concert listings from the webpage and parse all concerts

    Args:
        url (str): URL of the concert listings page

    Returns:
        list: List of dictionaries containing concert data
    """
    session = requests.Session()
    concerts = []

    try:
        # Fetch the page
        response = session.get(url)
        response.raise_for_status()

        # Parse the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all concert listings
        concert_divs = []
        all_concert_divs = soup.find_all(
            "div", class_="seetickets-list-event-container"
        )

        # Check if this div is NOT inside list-view-events
        for div in all_concert_divs:
            if not div.find_parent("div", id="list-view-events"):
                concert_divs.append(div)

        # Parse each concert listing
        for concert_div in concert_divs:
            concert_data = parse_concert_listing(concert_div)
            concerts.append(concert_data)

        return concerts

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    except Exception as e:
        print(f"Error parsing concert data: {e}")
        return None


def parse_concert_listing(concert_div) -> Concert:
    """
    Parse a single concert listing div and return structured data

    Args:
        concert_div (BeautifulSoup): BeautifulSoup object of a single concert listing

    Returns:
        dict: Concert
    """
    event_info = concert_div.find("div", class_="event-info-block")

    # Handle cases where elements might not exist
    try:
        ticket_link = concert_div.find("a", href=True)["href"]
    except (TypeError, KeyError):
        ticket_link = None

    try:
        image_url = concert_div.find("img", class_="seetickets-list-view-event-image")[
            "src"
        ]
    except (TypeError, KeyError):
        image_url = None

    try:
        show_time = event_info.find("span", class_="see-showtime").text.strip()
    except AttributeError:
        show_time = None

    if event_info.find("p", class_="date"):
        date = event_info.find("p", class_="date").text.strip()
        formatted_date = parse_concert_date(date)

    concert_data = {
        "title": (
            event_info.find("p", class_="title").text.strip()
            if event_info.find("p", class_="title")
            else None
        ),
        "date": (formatted_date if formatted_date else None),
        "headliner": (
            event_info.find("p", class_="headliners").text.strip()
            if event_info.find("p", class_="headliners")
            else None
        ),
        "venue": (
            event_info.find("p", class_="venue").text.strip().replace("at ", "")
            if event_info.find("p", class_="venue")
            else None
        ),
        "show_time": show_time,
        "ticket_url": ticket_link,
        "image_url": image_url,
    }

    return concert_data
