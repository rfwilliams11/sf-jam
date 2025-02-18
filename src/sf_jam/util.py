from datetime import datetime


def parse_concert_date(date_string):
    """
    Parse various concert date formats into a consistent datetime object.

    Args:
        date_string (str): The date string to parse

    Returns:
        datetime: A standardized datetime object
    """
    # Remove any extra whitespace
    date_string = date_string.strip()

    # List of possible date formats to try
    formats = [
        "%a %b %d",  # 'Fri Jan 24'
        "%b %d %a",  # 'Jan 24 Fri'
        "%a %b %d, %Y",  # 'Fri Jan 24, 2025'
        "%a, %b %d, %Y",  # 'Sat, Feb 1, 2025'
        "%m.%d %a",  # '2.17 Mon
    ]

    # Current year as fallback
    current_year = datetime.now().year

    for fmt in formats:
        try:
            # Try parsing with the current format
            parsed_date = datetime.strptime(date_string, fmt)

            # If no year is specified, use the current year
            if parsed_date.year == 1900:
                parsed_date = parsed_date.replace(year=current_year)

            return parsed_date.strftime("%a, %b %d, %Y")
        except ValueError:
            continue

    # If no format matches, raise an error
    raise ValueError(f"Unable to parse date string: {date_string}")
