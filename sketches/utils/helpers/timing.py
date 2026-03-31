from collections.abc import Generator
from contextlib import contextmanager
from datetime import datetime


@contextmanager
def report_time(title: str) -> Generator[None]:
    """Context manager que reporta o tempo de execução de um processo.

    :param title: Título do processo sendo medido.
    """
    start = datetime.now()
    msg = f"{title} started at {start}"
    print(msg, end=", ")
    yield
    finish = datetime.now()
    msg = f"ended at {finish} (took {(finish - start).seconds} seconds)"
    print(msg)
