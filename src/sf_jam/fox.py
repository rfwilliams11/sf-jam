from typing import List

from bs4 import BeautifulSoup
import requests
from concert import Concert
from headers import headers
from util import parse_concert_date


def retrieve_fox_concerts():
    """
    Retrieve concert listings from the Fox Theatre website

    Returns
        (List[Concert]): List of Concert objects
    """
    return fetch_and_parse_concerts("https://thefoxoakland.com/listing/")


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
        concert_divs = soup.find_all("div", class_="mix detail-information")
        # print(concert_divs)

        # Parse each concert listing
        for concert_div in concert_divs:
            concert_data = parse_concert_listing(concert_div)
            concerts.append(concert_data)
    except requests.RequestException as e:
        print(f"Error fetch {url}: {e}")
        return None
    except Exception as e:
        print(f"Error parsing concert data: {e}")
        return None

    return concerts


def parse_concert_listing(concert_div) -> Concert:

    # Extract title
    title = concert_div.find("h2", class_="show-title")
    title = title.text.strip() if title else None

    # Extract date
    formatted_date = None
    date_elem = concert_div.find("div", class_="date-show")
    if date_elem:
        formatted_date = parse_concert_date(date_elem.text.strip())

    # Extract time information
    time_elem = concert_div.find("div", class_="time-show")
    show_time = None
    if time_elem:
        show_time_elem = time_elem.find("span", class_="event__start-time")
        show_time = (
            show_time_elem.text.replace("Show:", "").strip() if show_time_elem else None
        )

    # Extract ticket and more info URLs
    ticket_url = concert_div.find("a", class_="button", text="Buy Tickets")
    ticket_url = ticket_url["href"] if ticket_url else None

    # Extract image URL
    image_elem = concert_div.find("img", class_="wp-post-image")
    image_url = image_elem["src"] if image_elem else None

    return {
        "title": title,
        "date": formatted_date,
        "headliner": title,
        "venue": "Fox Theatre",
        "show_time": show_time,
        "ticket_url": ticket_url,
        "image_url": image_url,
    }
