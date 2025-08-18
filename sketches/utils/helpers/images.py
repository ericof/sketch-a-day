from pathlib import Path
from PIL import Image

import numpy as np
import py5
import sketches
import tempfile


ROOT_FOLDER = Path(sketches.__file__).parent
RESOURCES_FOLDER = ROOT_FOLDER / "_resources"

__all__ = [
    "image_as_array",
    "resource_image_as_array",
    "save_frame",
]


def image_as_array(path: Path) -> np.ndarray:
    """Open an image file and return the Image object."""
    image = Image.open(path)
    return np.array(image)


def resource_image_as_array(filename: str) -> np.ndarray:
    """Open an image file from resources and return as numpy array."""
    path = RESOURCES_FOLDER / filename
    return image_as_array(path)


def tmp_path() -> Path:
    return Path(tempfile.mkdtemp())


def save_frame(tmp_path, img_name, frame) -> Path:
    path = tmp_path / f"{img_name}_{frame:03d}.png"
    py5.save_frame(path)
    return path
