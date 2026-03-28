from sketches import TEMPLATES_DIR
from sketches.utils.helpers.paths import sketch_path_for_day

import shutil


def create_new_sketch(day: str):
    """Create a new sketch from template."""
    src = TEMPLATES_DIR
    dst = sketch_path_for_day(day)
    # Create parent directories
    dst.parent.mkdir(parents=True, exist_ok=True)
    # Copy template directory
    shutil.copytree(src, dst, dirs_exist_ok=True)
    # Replace ##DAY## placeholder in __main__.py
    sketch_file = dst / "__main__.py"
    code = sketch_file.read_text()
    code = code.replace("##DAY##", day)
    sketch_file.write_text(code)
