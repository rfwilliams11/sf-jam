from typing import List

import requests
from bs4 import BeautifulSoup
from headers import headers
from models import Concert

from util import parse_concert_date


def retrieve_greek_concerts():
    """
    Retrieve concert listings from The Greek Theatre website

    Returns
        (List[Concert]): List of Concert objects
    """
    return fetch_and_parse_concerts("https://thegreekberkeley.com/event-listing/")


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
        concert_divs = soup.find_all("div", class_="content-information")

        # Parse each concert listing
        for concert_div in concert_divs:
            concert_data = parse_concert_listing(concert_div)
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
        dict: Concert data
    """
    event = {}

    # Extract date
    date_div = concert_div.select_one(".date-show")
    if date_div:
        concert_date = date_div.text.strip()  # Format: "Apr 04 Fri"
        event["date"] = parse_concert_date(concert_date)

    # Extract show time
    time_div = concert_div.select_one(".event__start-time")
    if time_div:
        event["show_time"] = time_div.text.replace("Show: ", "").strip()

    # Extract title/headliner
    title_elem = concert_div.select_one(".show-title")
    if title_elem:
        event["title"] = title_elem.text.strip()
        event["headliner"] = title_elem.text.strip()

    # Extract support acts
    support_div = concert_div.select_one(".support")
    if support_div:
        event["support"] = support_div.text.strip()

    # Extract ticket URL
    ticket_link = concert_div.select_one('.event-data a[href*="ticketmaster.com"]')
    if ticket_link:
        event["ticket_url"] = ticket_link["href"]

    # Extract image URL
    image = concert_div.select_one("img.wp-post-image")
    if image:
        event["image_url"] = image["src"]

    # Set venue
    event["venue"] = "The Greek Theatre"

    return event
