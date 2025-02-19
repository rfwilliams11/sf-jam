from typing import List

import requests
from bs4 import BeautifulSoup
from headers import headers
from models import Concert

from util import parse_concert_date


def retrieve_dunord_concerts():
    """
    Retrieve concert listings from the Cafe du Nord website

    Returns
        (List[Concert]): List of Concert objects
    """
    return fetch_and_parse_concerts("https://cafedunord.com/")


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

        # Find all concert listings within event-listing-container
        event_container = soup.find("div", class_="event-listing-container")
        concert_divs = (
            event_container.find_all("div", class_="tw-section")
            if event_container
            else []
        )

        # if concert_divs:
        # print(concert_divs[0])

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
    title_elem = concert_div.select_one(".tw-name span")
    if title_elem.text.strip() == "Private Event":
        return None
    if title_elem:
        event["title"] = title_elem.text.strip()
        event["headliner"] = title_elem.text.strip()

    # Extract date
    date_div = concert_div.select_one(".tw-event-datetime")
    if date_div:
        day = date_div.select_one(".tw-day-of-week").text.strip()
        date = date_div.select_one(".tw-event-date").text.strip()
        concert_date = f"{day} {date}"  # Format: "Tue 2.18"
        event["date"] = parse_concert_date(concert_date)

    # Extract show time
    time_div = concert_div.select_one(".tw-event-time")
    if time_div:
        event["show_time"] = time_div.text.replace("Show: ", "").strip()

    # Extract support acts
    support_div = concert_div.select_one(".tw-attractions span")
    if support_div:
        event["support"] = support_div.text.strip()

    # Extract ticket URL
    ticket_link = concert_div.select_one(".tw-buy-tix-btn")
    if ticket_link:
        event["ticket_url"] = ticket_link["href"]

    # Extract image URL
    image = concert_div.select_one("img.event-img")
    if image:
        event["image_url"] = image["src"]

    # Set venue
    event["venue"] = "Cafe du Nord"

    return event
