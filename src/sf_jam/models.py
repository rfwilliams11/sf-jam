from dataclasses import dataclass
from typing import List, Dict, Callable


@dataclass
class VenueConfig:
    """Configuration for a venue's scraping operation."""

    name: str
    retrieval_func: Callable[[], List[Dict]]
    db_name: str


@dataclass
class Concert:
    title: str
    date: str
    headliner: str
    venue: str
    age_restriction: str
    price_range: str
    genre: str
    door_time: str
    show_time: str
    ticket_url: str
    image_url: str
