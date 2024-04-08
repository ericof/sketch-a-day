from datetime import date, timedelta


def process_day(day: str) -> str:
    """Handle relative dates."""
    day = day.lower()
    today = date.today()
    if day == "today":
        day = f"{today}"
    elif day == "yesterday":
        day = f"{today + timedelta(day=-1)}"
    elif day == "tomorrow":
        day = f"{today + timedelta(day=1)}"
    return day


def format_day(day: str) -> str:
    """Process day to be used for a repo module."""
    day = process_day(day)
    return f"d{day.replace('-', '_')}"
