from pathlib import Path

import numpy as np
import py5
from PIL import Image

from utils.data import SketchInfo

from .sketches import info_for_sketch  # noQA
from .sketches import sketch_for_day  # noQA
from .sketches import sketch_info_for_day  # noQA

LARGURA = 800
ALTURA = 800


def image_as_array(path: Path) -> np.array:
    """Open an image file and return the Image object."""
    image = Image.open(path)
    return np.array(image)


def write_legend(sketch: SketchInfo, cor: str = "#FFF"):
    py5.fill(cor)
    py5.text_size(16)
    py5.text_align(py5.RIGHT)
    py5.text(sketch.title, LARGURA - 30, ALTURA - 30)


def save_sketch_image(sketch: SketchInfo):
    img_path = sketch.path / f"{sketch.day}.{sketch.format}"
    img = py5.get_pixels(0, 0, LARGURA, ALTURA)
    img.save(img_path)
