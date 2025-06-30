from datetime import date
from datetime import datetime
from git import Actor
from git import Commit
from git import Repo
from pathlib import Path
from random import choice
from sketches.utils.data import SketchInfo
from sketches.utils.helpers.repo import get_repo
from zoneinfo import ZoneInfo

import subprocess


def _author() -> Actor:
    """Return the author of the commit."""
    return Actor("Érico Andrei", "ericof@gmail.com")


def _commit_date_for_skecth(info: SketchInfo) -> datetime:
    day = info.day.day
    month = info.day.month
    year = info.day.year
    tz = ZoneInfo("America/Sao_Paulo")
    if date.today() == info.day:
        commit_date = datetime.now(tz=tz)
    else:
        hours = range(0, 23)
        minutes = range(0, 59)
        seconds = range(0, 59)
        commit_date = datetime(
            year,
            month,
            day,
            choice(hours),  # noQA: S311
            choice(minutes),  # noQA: S311
            choice(seconds),  # noQA: S311
            tzinfo=tz,
        )
    return commit_date


def _add_files_to_index(repo: Repo, files: list[Path]) -> None:
    """Add files to the git index."""
    for file in files:
        if file.exists():
            repo.git.add([str(file)])  # Add file to staging area
        else:
            print(f"Warning: {file} does not exist and will not be added.")


def _run_linter() -> bool:
    """Run the linter on the codebase."""
    try:
        subprocess.run("make lint", shell=True, check=True)  # noQA: S602,S607
    except subprocess.CalledProcessError:
        return False  # Linter failed
    else:
        return True


def commit_changes(info: SketchInfo) -> Commit:
    """Commit code into repository, return the commit object."""
    repo = get_repo()
    index = repo.index

    readme = Path("README.md").resolve()
    sketch_path = info.path.resolve()
    files = [readme, sketch_path]
    _add_files_to_index(repo, files)  # Add files to staging area
    if not _run_linter():
        # Pre-commit linter probably fixed some issues, let's run it again
        _add_files_to_index(repo, files)  # Add files to staging area
        if not _run_linter():
            raise RuntimeError(
                "Linter failed. Please fix the issues before committing."
            )

    # Prepare commit message
    commit_date = _commit_date_for_skecth(info)
    commit_message = f"Sketch for {info.day:%Y-%m-%d}"
    author = _author()
    commit = index.commit(
        commit_message,
        author=author,
        committer=author,
        commit_date=commit_date,
        author_date=commit_date,
    )
    return commit
