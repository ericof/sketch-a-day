from pathlib import Path

from utils.data import SketchInfo

PLACEHOLDER = "<!-- Next Item -->"


def update_readme(info: SketchInfo):
    """Update readme file."""
    readme = Path("./README.md").resolve()
    text = readme.read_text()
    path = f"./sketches/{info.day:d%Y_%m_%d}"
    # | Day | Title | File | Image |
    day_formatted = f"{info.day:%Y-%m-%d}"
    day = f"[{day_formatted}]({path})"
    title = f"{info.title}"
    code_file = f"[{path}/.__main__.py]({path}/.__main__.py)"
    image = f"![{day_formatted}]({path}/{info.filename})"
    linha = f"| {day} | {title} | {code_file} | {image} |\n{PLACEHOLDER}\n"
    if linha in text:
        # Line already there
        return readme
    text = text.replace(PLACEHOLDER, linha)
    readme.write_text(text)
    return readme
