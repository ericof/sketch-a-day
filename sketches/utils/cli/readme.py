from pathlib import Path
from sketches.utils.data import SketchInfo
from sketches.utils.helpers.paths import sketch_path_for_day


PLACEHOLDER = "<!-- Next Item -->"


def update_readme(info: SketchInfo):
    """Update readme file."""
    readme = Path("./README.md").resolve()
    text = readme.read_text()
    path = sketch_path_for_day(f"{info.day:%Y-%m-%d}")
    # | Day | Description | File | Image |
    day_formatted = f"{info.day:%Y-%m-%d}"
    day = f"[{day_formatted}]({path})"
    description = f"{info.description}"
    code_file = f"[{path}/__main__.py]({path}/__main__.py)"
    image = f"![{day_formatted}]({path}/{info.filename})"
    linha = f"| {day} | {description} | {code_file} | {image} |\n{PLACEHOLDER}"
    if linha in text:
        # Line already there
        return readme
    text = text.replace(PLACEHOLDER, linha)
    readme.write_text(text)
    return readme
