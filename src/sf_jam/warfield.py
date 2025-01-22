from typing import List

from bs4 import BeautifulSoup
import requests
from concert import Concert


def retrieve_warfield_concerts():
    """
    Retrieve concert listings from The Warfield website

    Returns
        (List[Concert]): List of Concert objects
    """
    return fetch_and_parse_concerts("https://www.thewarfieldtheatre.com/events")


def fetch_and_parse_concerts(url: str) -> List[Concert]:
    """
    Fetch concert listings from the webpage and parse all concerts

    Args:
        url (str): URL of the concert listings page

    Returns:
        list: List of dictionaries containing concert data
    """
    sessions = requests.Session()
    concerts = []

    try:
        # Fetch the page
        response = sessions.get(url)
        response.raise_for_status()

        # Parse the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all concert listings
        concert_divs = soup.find_all(
            "div",
            class_=lambda x: x and "warfield" in x.split() and "clearfix" in x.split(),
        )

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
    Parse a single concert listing div and extract the concert data

    Args:
        concert_div (BeautifulSoup): A single concert listing div

    Returns:
        dict: Concert
    """

    # Initialize Concert with default None values
    event_data = {
        "title": None,
        "date": None,
        "headliner": None,
        "venue": "The Warfield",  # Default value
        "age_restriction": None,  # Not present in HTML
        "price_range": None,  # Not present in HTML
        "genre": None,  # Not present in HTML
        "door_time": None,  # Not in HTML
        "show_time": None,
        "ticket_url": None,
        "image_url": None,
    }

    # Get image URL
    img_tag = concert_div.find("img")
    if img_tag and img_tag.get("src"):
        event_data["image_url"] = img_tag["src"]

    # Get ticket URL
    ticket_link = concert_div.find("a", class_="btn-tickets")
    if ticket_link:
        event_data["ticket_url"] = ticket_link["href"]

    # Get title/headliner (using the main title, not "Goldenvoice Presents")
    title_tag = concert_div.find("h3", class_="carousel_item_title_small")
    if title_tag and title_tag.a:
        headliner = title_tag.a.text.strip()
        event_data["title"] = headliner
        event_data["headliner"] = headliner

    # Get date and show time
    date_container = concert_div.find("div", class_="date-time-container")
    if date_container:
        date_span = date_container.find("span", class_="date")
        if date_span:
            event_data["date"] = date_span.text.strip().replace("Fri, ", "Fri ")

        time_span = date_container.find("span", class_="time")
        if time_span:
            show_time = time_span.text.strip().replace("Show", "").strip()
            event_data["show_time"] = show_time

    return event_data
