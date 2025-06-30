from sketches import DAILY_DIR
from sketches import TEMPLATES_DIR
from sketches.utils.helpers.dates import format_day

import shutil


def create_new_sketch(day: str):
    """Create a new sketch from template."""
    formatted_day = format_day(day)
    src = TEMPLATES_DIR
    dst = DAILY_DIR / formatted_day
    # Copy template directory
    shutil.copytree(src, dst)
    # Replace ##DAY## placeholder in __main__.py
    sketch_file = dst / "__main__.py"
    code = sketch_file.read_text()
    code = code.replace("##DAY##", day)
    sketch_file.write_text(code)
