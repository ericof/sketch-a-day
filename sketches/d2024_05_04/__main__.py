"""2024-05-04
May the 4th
Pixelado de poster japonês de Star Wars
png
Sketch,py5,CreativeCoding,maythe4th
"""

from pathlib import Path

import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def pixelate(img_array):
    py5.no_stroke()
    slots = [int(c) for c in np.logspace(0.202, 1.215, num=70, endpoint=False)]
    slots = sorted(slots, reverse=True) + slots
    x = 0
    for chunk_x in slots:
        y = 0
        for chunk_y in slots:
            block = img_array[y : y + chunk_y, x : x + chunk_x]
            avg_color = np.median(block, axis=(0, 1))
            py5.fill(avg_color[0], avg_color[1], avg_color[2], 100)
            py5.rect(x, y, chunk_x, chunk_y)
            y += chunk_y
        x += chunk_x


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA)
    py5.background(0)
    path = Path(__file__).parent / "poster.jpg"
    img_array = helpers.image_as_array(path)
    pixelate(img_array)
    helpers.write_legend(sketch=sketch, cor="#000", frame="#FFF")


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
