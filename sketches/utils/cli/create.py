from sketches import DAILY_DIR
from sketches import TEMPLATES_DIR
from sketches.utils.helpers.dates import format_day
from sketches.utils.helpers.dates import format_year_month

import shutil


def create_new_sketch(day: str):
    """Create a new sketch from template."""
    formatted_year_month = format_year_month(day)
    formatted_day = format_day(day)
    src = TEMPLATES_DIR
    dst = DAILY_DIR / formatted_year_month / formatted_day
    # Create parent directories
    dst.parent.mkdir(parents=True, exist_ok=True)
    # Copy template directory
    shutil.copytree(src, dst, dirs_exist_ok=True)
    # Replace ##DAY## placeholder in __main__.py
    sketch_file = dst / "__main__.py"
    code = sketch_file.read_text()
    code = code.replace("##DAY##", day)
    sketch_file.write_text(code)
