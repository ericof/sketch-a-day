"""2023-10-31"""
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


def _pixelate(img_array, x, chunks):
    for pixel_chunk in chunks:
        pixel_chunk = int(pixel_chunk)
        for y in range(0, HEIGHT, pixel_chunk):
            block = img_array[y : y + pixel_chunk, x : x + pixel_chunk]
            avg_color = np.max(block, axis=(0, 1))
            stroke = [c * STROKE_MOD for c in avg_color]
            py5.stroke(py5.color(*stroke, 100))
            py5.fill(py5.color(*avg_color, 100))
            py5.rect(x, y, pixel_chunk, pixel_chunk)
        x += pixel_chunk
    return x


def pixelate(img_array):
    meio = WIDTH // 2
    x = 0
    pixel_chunks = np.logspace(1.7, 0.1, num=15)
    x = _pixelate(img_array, x, pixel_chunks)
    diff = meio - x
    x_final = meio + diff
    py5.no_stroke()
    for x in range(x, x_final):
        pixel_size = 1
        for y in range(0, HEIGHT, pixel_size):
            block = img_array[y : y + pixel_size, x : x + pixel_size]
            colors = block[0][0]
            py5.fill(*colors, 100)
            py5.rect(x, y, pixel_size, pixel_size)
    pixel_chunks = sorted(pixel_chunks, reverse=False)
    x = _pixelate(img_array, x_final, pixel_chunks)
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
