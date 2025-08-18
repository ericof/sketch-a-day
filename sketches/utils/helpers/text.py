from pathlib import Path

import sketches


ROOT_FOLDER = Path(sketches.__file__).parent
RESOURCES_FOLDER = ROOT_FOLDER / "_resources"


def resource_text(filename: str) -> str:
    """Open a text file from the resource folder."""
    path = RESOURCES_FOLDER / filename
    return path.read_text()
