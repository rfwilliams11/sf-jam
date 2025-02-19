from typing import List

import requests
from bs4 import BeautifulSoup
from headers import headers
from models import Concert

from util import parse_concert_date


def retrieve_great_american_concerts():
    """
    Retrieve concert listings from the Great American Music Hall website

    Returns
        (List[Concert]): List of Concert objects
    """
    return fetch_and_parse_concerts("https://gamh.com/calendar/")


def fetch_and_parse_concerts(url: str) -> List[Concert]:
    """
    Fetch concert listings from the webpage and parse all concerts

    Args:
        url (str): URL of the concert listings page

    Returns:
        list: List of Concert objects
    """
    sessions = requests.Session()
    concerts = []

    try:
        # Fetch the page
        response = sessions.get(url, headers=headers)
        response.raise_for_status()

        # Parse the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all concert listings
        concert_divs = soup.find_all("div", class_="seetickets-list-event-container")

        # Parse each concert listing
        for concert_div in concert_divs:
            concert_data = parse_concert_listing(concert_div)
            if concert_data:
                concerts.append(concert_data)

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    except Exception as e:
        print(f"Error parsing concert data: {e}")
        return None

    return concerts


def parse_concert_listing(concert_div) -> Concert:
    """
    Parse a single concert listing div and extract the concert data

    Args:
        concert_div (BeautifulSoup): A single concert listing div

    Returns:
        Concert: Concert data
    """
    event = {}

    # Extract title/headliner
    title_elem = concert_div.select_one(".event-title a")
    if title_elem:
        event["title"] = title_elem.text.strip()

    # Extract headliner (separate from title as it might be different)
    headliner_elem = concert_div.select_one(".headliners")
    if headliner_elem:
        event["headliner"] = headliner_elem.text.strip()

    # Extract support acts
    support_elem = concert_div.select_one(".supporting-talent")
    if support_elem and support_elem.text.strip():
        event["support"] = support_elem.text.strip()

    # Extract date
    date_elem = concert_div.select_one(".event-date")
    if date_elem:
        event["date"] = parse_concert_date(date_elem.text.strip())

    # Extract show time and door time
    time_elem = concert_div.select_one(".doortime-showtime")
    if time_elem:
        door_time = time_elem.select_one(".see-doortime")
        show_time = time_elem.select_one(".see-showtime")
        if door_time:
            event["door_time"] = door_time.text.strip()
        if show_time:
            event["show_time"] = show_time.text.strip()

    # Extract ticket URL
    ticket_link = concert_div.select_one(".seetickets-buy-btn")
    if ticket_link:
        event["ticket_url"] = ticket_link["href"]

    # Extract image URL
    image = concert_div.select_one(".seetickets-list-view-event-image")
    if image:
        event["image_url"] = image["src"]

    # Set venue
    event["venue"] = "Great American"

    return event
