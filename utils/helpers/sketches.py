from importlib import import_module
from pathlib import Path

from utils.data import Sketch, SketchInfo


def info_for_sketch(__file, __doc) -> SketchInfo:
    """Information about this sketch."""
    doc_parts = __doc.split("\n")
    title, description, alt, format, tags = doc_parts[:5]
    tags = tags.split(",")
    parent_folder = Path(__file).parent
    return SketchInfo(
        path=parent_folder,
        title=title,
        description=description,
        alt=alt,
        format=format,
        tags=tags,
    )


def sketch_info_for_day(day: str) -> SketchInfo:
    """Return the SketchInfo for a given day."""
    formatted_day = f"d{day.replace('-', '_')}"
    mod = import_module(f"sketches.{formatted_day}.__main__")
    return mod.sketch


def sketch_for_day(day: str) -> Sketch:
    """Return the Sketch for a given day."""
    from .repo import commit_date_for_day

    info = sketch_info_for_day(day)
    commit_date = commit_date_for_day(day)
    return Sketch(info=info, commit_date=commit_date)
