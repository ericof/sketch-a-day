import tempfile
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


def write_legend(
    sketch: SketchInfo, cor: str = "#FFF", tamanho: int = 16, frame: str = ""
):
    with py5.push_style():
        if frame:
            py5.fill(frame)
            py5.rect_mode(py5.CORNERS)
            py5.rect(LARGURA - 110, ALTURA - 50, LARGURA - 20, ALTURA - 20)
        py5.fill(cor)
        py5.text_size(tamanho)
        py5.text_align(py5.RIGHT)
        py5.text(sketch.title, LARGURA - 30, ALTURA - 30)


def save_sketch_image(sketch: SketchInfo):
    img_path = sketch.path / f"{sketch.day}.{sketch.format}"
    img = py5.get_pixels(0, 0, LARGURA, ALTURA)
    img.save(img_path)


def tmp_path() -> Path:
    return Path(tempfile.mkdtemp())


def save_frame(tmp_path, img_name, frame) -> Path:
    path = tmp_path / f"{img_name}_{frame:03d}.png"
    py5.save_frame(path)
    return path
