from datetime import date
from datetime import timedelta


def process_day(day: str) -> str:
    """Handle relative dates."""
    day = day.lower()
    today = date.today()
    if day == "today":
        day = f"{today}"
    elif day == "yesterday":
        day = f"{today + timedelta(days=-1)}"
    elif day == "tomorrow":
        day = f"{today + timedelta(days=1)}"
    return day


def format_year_month(day: str) -> str:
    """Process date to be used for a repo module."""
    day = process_day(day)
    return f"y{day[:4]}_m{day[5:7]}"


def format_day(day: str) -> str:
    """Process day to be used for a repo module."""
    day = process_day(day)
    return f"d{day[8:10]}"
