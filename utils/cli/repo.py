import subprocess
from datetime import date, datetime
from random import choice

from utils.data import SketchInfo


def commit_changes(info: SketchInfo):
    """Commit code into repository."""
    day = info.day.day
    month = info.day.month
    year = info.day.year
    if date.today() == info.day:
        commit_date = datetime.now()
    else:
        hours = range(0, 23)
        minutes = range(0, 59)
        seconds = range(0, 59)
        commit_date = datetime(
            year, month, day, choice(hours), choice(minutes), choice(seconds)
        )

    formatted = f"{commit_date:%a %d %b %Y %H:%M:%S} +0300".upper()
    readme = "README.md"
    path = info.path.resolve()

    cmds = [
        f"git add {readme} {path}",
        (
            f'GIT_COMMITTER_DATE="{formatted}" '
            f'git commit --date "{formatted}" -m "Sketch for {info.day:%Y-%m-%d}"'
        ),
    ]
    for cmd in cmds:
        print(f"Running {cmd}")
        subprocess.run(cmd, shell=True, check=True)
