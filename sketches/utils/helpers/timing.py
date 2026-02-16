from contextlib import contextmanager
from datetime import datetime


@contextmanager
def report_time(title: str):
    """Context manager to report the start and end time of a process."""
    start = datetime.now()
    msg = f"{title} started at {start}"
    print(msg, end=", ")
    yield
    finish = datetime.now()
    msg = f"ended at {finish} (took {(finish - start).seconds} seconds)"
    print(msg)
