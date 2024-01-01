from datetime import datetime
from pathlib import Path

from git import Repo


def get_repo() -> Repo:
    """GIT Repository for this codebase."""
    path = Path(__file__).parent.parent.parent
    return Repo.init(path)


def commit_date_for_day(day: str) -> datetime:
    """Return commit date for a given day."""
    base_path = Path(__file__).parent.parent.parent
    repo = get_repo()
    formatted_day = f"d{day.replace('-', '_')}"
    path = f"{base_path}/sketches/{formatted_day}"
    all_commits = list(repo.iter_commits(all=True, max_count=10, paths=path))
    last_commit = all_commits[0] if all_commits else None
    if not last_commit:
        return
    commit_date = datetime.fromtimestamp(last_commit.committed_date)
    return commit_date
