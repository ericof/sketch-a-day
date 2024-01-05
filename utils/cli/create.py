import shutil
from pathlib import Path


def create_new_sketch(day: str):
    """Create a new sketch from template."""
    formatted_day = f"d{day.replace('-', '_')}"
    src = Path(".") / "sketches" / "_template"
    dst = Path(".") / "sketches" / formatted_day
    # Copy template directory
    shutil.copytree(src, dst)
    # Replace ##DAY## placeholder in __main__.py
    sketch_file = dst / "__main__.py"
    code = sketch_file.read_text()
    code = code.replace("##DAY##", day)
    sketch_file.write_text(code)
