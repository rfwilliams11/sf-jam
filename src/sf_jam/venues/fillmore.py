from typing import List
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from models import Concert
from headers import headers
from util import parse_concert_date


def retrieve_fillmore_concerts():
    """
    Retrieve concert listings from The Fillmore website

    Returns:
        (List[Concert]): List of Concert objects
    """

    return fetch_and_parse_concerts(
        "https://www.ticketmaster.com/the-fillmore-tickets-san-francisco/venue/229424"
    )


def fetch_and_parse_concerts(url: str) -> List[Concert]:
    """
    Fetch concert listings from the webpage and parse all concerts

    Args:
        url (str): URL of the concert listings page

    Returns:
        list: List of Concert objects
    """
    session = requests.Session()
    concerts = []

    try:
        # Fetch the page
        response = session.get(url, headers=headers)
        # print(response.status_code)
        response.raise_for_status()

        # Parse the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all concert listings
        concert_divs = soup.find_all("div", class_="sc-fyofxi-0 MDVIb")

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
    event = {}

    # Extract date and convert to desired format with day of week
    month_span = concert_div.select_one(".sc-1evs0j0-1 span")
    day_span = concert_div.select_one(".sc-1evs0j0-2 span")
    if month_span and day_span:
        month = month_span.text
        day = day_span.text
        # Get the year from the hidden span that contains full date
        full_date_span = concert_div.select_one(".VisuallyHidden-sc-8buqks-0 span")
        year = "2025"  # Default to 2025 if not found
        if full_date_span:
            # Extract year from format like "1/24/25"
            date_text = full_date_span.text.strip()
            if "/" in date_text:
                year = "20" + date_text.split("/")[-1]

        # Create datetime object to get day of week
        try:
            date_obj = datetime.strptime(f"{month} {day} {year}", "%b %d %Y")
            date = date_obj.strftime("%a %b %d")  # Format: "Fri Jan 24"
            formatted_date = parse_concert_date(date)
            event["date"] = formatted_date
        except ValueError:
            event["date"] = f"{month} {day}"  # Fallback to original format

    # Extract show time
    time_span = concert_div.select_one(".sc-1idcr5x-1 span")
    if time_span:
        event["show_time"] = time_span.text

    # Extract title/headliner
    title_span = concert_div.select_one(".sc-fyofxi-5")
    if title_span:
        event["title"] = title_span.text
        event["headliner"] = title_span.text

    # Extract ticket URL
    ticket_link = concert_div.select_one('a[data-testid="event-list-link"]')
    if ticket_link:
        event["ticket_url"] = ticket_link["href"]
        # Optionally fetch additional details from ticket page
        # try:
        #     event.update(fetch_ticket_details(event["ticket_url"]))
        # except Exception as e:
        #     print(f"Error fetching ticket details: {e}")

    # Initialize fields that aren't in the provided HTML
    event.setdefault("venue", "The Fillmore")
    event.setdefault("image_url", None)

    return event


# def fetch_ticket_details(ticket_url):
#     """
#     Fetch additional details from the ticket page

#     Args:
#         ticket_url (str): URL of the ticket page

#     Returns:
#         dict: Additional event details
#     """

#     try:
#         response = requests.get(ticket_url, headers=headers)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, "html.parser")

#         details = {}

#         # Note: These selectors would need to be adjusted based on the actual ticket page HTML structure
#         # This is just an example of what could be extracted

#         # Example price range extraction (adjust selectors as needed)
#         price_elem = soup.select_one(".price-range")  # Adjust selector
#         if price_elem:
#             details["price_range"] = price_elem.text.strip()

#         # Example age restriction extraction
#         age_elem = soup.select_one(".age-restriction")  # Adjust selector
#         if age_elem:
#             details["age_restriction"] = age_elem.text.strip()

#         return details

#     except Exception as e:
#         print(f"Error fetching ticket page: {e}")
#         return {}
