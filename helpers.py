from PIL import Image
from pathlib import Path
import tempfile

import py5


WIDTH = 800
HEIGHT = 800


def write_legend(palette=None, img_name=""):
    if palette:
        color = palette[-1]
    else:
        color = "#000"
    py5.fill(color)
    py5.text_size(12)
    py5.text_align(py5.RIGHT)
    py5.text(img_name, WIDTH - 20, HEIGHT - 20)


def save_image(img_name, extension="jpg"):
    folder = Path(__file__).parent.resolve()
    img_folder = folder / "Images"
    img_path = img_folder / f"{img_name}.{extension}"
    img = py5.get(0, 0, WIDTH, HEIGHT)
    img.save(img_path)


def tmp_path() -> Path:
    return Path(tempfile.mkdtemp())


def save_frame(tmp_path, img_name, frame) -> Path:
    path = tmp_path / f"{img_name}_{frame:03d}.tga"
    py5.save_frame(path)
    return path


def save_gif(img_name, frames, duration: int = 200, loop=0):
    folder = Path(__file__).parent.resolve()
    img_folder = folder / "Images"
    img_path = img_folder / f"{img_name}.gif"
    images = [Image.open(frame) for frame in frames]
    kw = {
        "save_all": True,
        "append_images": images[1:],
        "duration": duration,
        "optimize": True,
    }
    if loop is not None:
        kw["loop"] = loop
    images[0].save(img_path, **kw)
