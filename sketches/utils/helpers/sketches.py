from datetime import datetime
from git import Commit
from importlib import import_module
from pathlib import Path
from sketches.utils.data import Sketch
from sketches.utils.data import SketchInfo
from sketches.utils.data import SketchSize
from sketches.utils.helpers.dates import format_day
from sketches.utils.helpers.dates import format_year_month


DIMENSOES = SketchSize(
    external=(1000, 1000),
    internal=(800, 800),
)


def info_for_sketch(__file, __doc) -> SketchInfo:
    """Information about this sketch."""
    doc_parts = __doc.split("\n")
    title, description, alt, other_credits, format_, tags = doc_parts[:6]
    other_credits = other_credits.replace("|", "\n")
    tags = tags.split(",")
    parent_folder = Path(__file).parent
    return SketchInfo(
        path=parent_folder,
        title=title,
        description=description,
        other_credits=other_credits,
        alt=alt,
        format=format_,
        tags=tags,
        size=DIMENSOES,
    )


def sketch_info_for_day(day: str) -> SketchInfo:
    """Return the SketchInfo for a given day."""
    formatted_year_month = format_year_month(day)
    formatted_day = format_day(day)
    mod = import_module(
        f"sketches.daily.{formatted_year_month}.{formatted_day}.__main__"
    )
    return mod.sketch


def sketch_for_day(day: str, commit: Commit | None = None) -> Sketch:
    """Return the Sketch for a given day."""
    from .repo import last_commit_for_day

    info = sketch_info_for_day(day)
    if not commit:
        commit = last_commit_for_day(day)
    commit_date = datetime.fromtimestamp(commit.committed_date) if commit else None
    commit_hash = commit.hexsha if commit else None
    return Sketch(info=info, commit_hash=commit_hash, commit_date=commit_date)
