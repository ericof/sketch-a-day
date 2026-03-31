from datetime import datetime
from git import Commit
from git import Repo
from pathlib import Path
from sketches.utils.helpers.dates import format_day
from sketches.utils.helpers.dates import format_year_month


def get_repo() -> Repo:
    """Retorna o repositório Git deste codebase."""
    import sketches

    path = Path(sketches.__file__).parent.parent
    return Repo.init(path)


def get_last_commit_for_file(repo: Repo, filepath: Path) -> Commit | None:
    """Retorna o último commit que modificou o arquivo informado.

    :param repo: Repositório Git.
    :param filepath: Caminho absoluto ou relativo do arquivo.
    :returns: Último commit que modificou o arquivo, ou None.
    """
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
    """Retorna o último commit do sketch de um dia específico.

    :param day: Data em formato ISO ou relativa.
    :returns: Último commit do sketch, ou None.
    """
    repo = get_repo()
    formatted_year_month = format_year_month(day)
    formatted_day = format_day(day)
    path = f"sketches/daily/{formatted_year_month}/{formatted_day}"
    last_commit = get_last_commit_for_file(repo, Path(path))
    return last_commit


def commit_date_for_day(day: str) -> datetime | None:
    """Retorna a data do último commit do sketch de um dia específico.

    :param day: Data em formato ISO ou relativa.
    :returns: Data do commit, ou None se não houver commit.
    """
    last_commit = last_commit_for_day(day)
    if not last_commit:
        return
    commit_date = datetime.fromtimestamp(last_commit.committed_date)
    return commit_date
