from datetime import datetime
from git import Commit
from git import Repo
from pathlib import Path


def get_repo() -> Repo:
    """GIT Repository for this codebase."""
    import sketches

    path = Path(sketches.__file__).parent.parent
    return Repo.init(path)


def get_last_commit_for_file(repo: Repo, filepath: Path) -> Commit | None:
    """Returns the last commit that modified the given file in a Git repository."""
    # Iterate through commits in reverse chronological order
    base_path = Path(repo.git_dir).parent
    filepath = filepath.resolve()
    rel_path = str(filepath.relative_to(base_path))
    for commit in repo.iter_commits():
        try:
            # Check if the file exists in the tree of the current commit
            commit.tree[rel_path]
            return commit  # Found the last commit affecting the file
        except KeyError:
            # File not found in this commit's tree, continue to the
            # previous commit
            pass
    return None


def last_commit_for_day(day: str) -> Commit | None:
    """Return commit date for a given day."""
    repo = get_repo()
    formatted_day = f"d{day.replace('-', '_')}"
    path = f"sketches/daily/{formatted_day}"
    last_commit = get_last_commit_for_file(repo, Path(path))
    return last_commit


def commit_date_for_day(day: str) -> datetime | None:
    """Return commit date for a given day."""
    last_commit = last_commit_for_day(day)
    if not last_commit:
        return
    commit_date = datetime.fromtimestamp(last_commit.committed_date)
    return commit_date
