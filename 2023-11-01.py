"""2023-11-01"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from PIL import Image

import numpy as np
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

STROKE_MOD = 0.75


def setup():
    py5.size(WIDTH, HEIGHT)
    path = Path(__name__).parent.resolve() / "resources"
    image = Image.open(path / "torii.jpg")
    img_array = np.array(image)

    pixelate(img_array)
    write_legend([py5.color(0)], IMG_NAME)


def _pixelate(img_array, x, chunks, limite):
    for pixel_chunk in chunks:
        pixel_chunk = int(pixel_chunk)
        for y in range(0, HEIGHT, pixel_chunk):
            block = img_array[y : y + pixel_chunk, x : x + pixel_chunk]
            avg_color = np.max(block, axis=(0, 1))
            stroke = [c * STROKE_MOD for c in avg_color]
            py5.stroke(py5.color(*stroke, 100))
            py5.fill(py5.color(*avg_color, 100))
            py5.circle(x, y, pixel_chunk * 1.1)
        x += pixel_chunk
        if x >= limite:
            return x
    return x


def pixelate(img_array):
    x = 0
    pixel_chunks = np.logspace(0.4, 1.01, num=80)
    x = _pixelate(img_array, x, pixel_chunks, 400)
    pixel_chunks = sorted(pixel_chunks, reverse=True)
    x = _pixelate(img_array, x, pixel_chunks, 800)
    print(x)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
