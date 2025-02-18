from typing import List

import requests
from bs4 import BeautifulSoup
from headers import headers
from models import Concert

from util import parse_concert_date


def retrieve_independent_concerts():
    """
    Retrieve concert listings from The Independent website

    Returns
        (List[Concert]): List of Concert objects
    """
    return fetch_and_parse_concerts("https://www.theindependentsf.com/")


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
        concert_divs = soup.find_all("div", class_="tw-section")

        # if concert_divs:
        # print(concert_divs[0])

        # Parse each concert listing
        for concert_div in concert_divs:
            # print(concert_div)
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
        dict: Concert data
    """
    event = {}

    # Extract date
    date_elem = concert_div.select_one(".tw-event-date-complete")

    if not date_elem:
        return None  # Skip this concert if no date is found

    if date_elem:
        day_of_week = concert_div.select_one(".tw-day-of-week").text.strip()
        date = date_elem.select_one(".tw-event-date").text.strip()

        if not (day_of_week and date):
            return None  # Skip if either component is missing

        concert_date = f"{date} {day_of_week}"  # Format: "2.17 Mon"
        event["date"] = parse_concert_date(concert_date)

    # Extract show time
    time_elem = concert_div.select_one(".tw-event-time")
    if time_elem:
        event["show_time"] = time_elem.text.strip()

    # Extract title/headliner
    title_elem = concert_div.select_one(".tw-name a")
    if title_elem:
        event["title"] = title_elem.text.strip()
        event["headliner"] = title_elem.text.strip()

    # Extract support acts
    support_elem = concert_div.select_one(".tw-artist.tw-support")
    if support_elem:
        event["support"] = support_elem.text.strip()

    # Extract ticket URL
    ticket_link = concert_div.select_one(".tw-buy-tix-btn")
    if ticket_link and ticket_link.has_attr("href"):
        event["ticket_url"] = ticket_link["href"]
    else:
        event["ticket_url"] = None

    # Extract image URL
    image = concert_div.select_one(".tw-image img")
    if image and image.has_attr("src"):
        event["image_url"] = image["src"]
    else:
        event["image_url"] = None

    # Set venue
    event["venue"] = "The Independent"

    return event
