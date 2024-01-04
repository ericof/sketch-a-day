"""2024-01-04
Genuary 04 - Pixels.
Foto pixelada de um Torii da ilha de Myiajima.
png
Sketch,py5,CreativeCoding,genuary,genuary4
"""
from pathlib import Path

import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def pixelate(img_array):
    pixel_chunk = 24
    py5.stroke_weight(1)
    py5.stroke(20, 20, 20)
    for x in range(0, helpers.LARGURA, pixel_chunk):
        pixel_size = pixel_chunk
        for y in range(0, helpers.ALTURA, pixel_size):
            if y + pixel_size > helpers.ALTURA:
                pixel_size = helpers.ALTURA - y

            block = img_array[y : y + pixel_size, x : x + pixel_chunk]
            avg_color = np.median(block, axis=(0, 1))
            py5.fill(avg_color[0], avg_color[1], avg_color[2], 100)
            py5.rect(x, y, pixel_chunk, pixel_size)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P2D)
    py5.background(0)
    path = Path(__file__).parent / "torii.jpg"
    img_array = helpers.image_as_array(path)
    pixelate(img_array)
    helpers.write_legend(sketch=sketch)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    helpers.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
