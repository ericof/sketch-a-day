from pathlib import Path
from PIL import Image

import numpy as np
import py5
import tempfile


__all__ = [
    "image_as_array",
    "save_frame",
]


def image_as_array(path: Path) -> np.array:
    """Open an image file and return the Image object."""
    image = Image.open(path)
    return np.array(image)


def tmp_path() -> Path:
    return Path(tempfile.mkdtemp())


def save_frame(tmp_path, img_name, frame) -> Path:
    path = tmp_path / f"{img_name}_{frame:03d}.png"
    py5.save_frame(path)
    return path
