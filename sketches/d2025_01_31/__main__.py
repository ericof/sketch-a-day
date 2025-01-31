"""2025-01-31
Pixel sorting (RGB Average)
Reutiliza sketch de 2025-01-16.
png
Sketch,py5,CreativeCoding,genuary,genuary31
"""

from pathlib import Path

import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def carrega_imagem(nome: str):
    path = Path(__file__).parent / nome
    return helpers.image_as_array(path)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    array = carrega_imagem("2025-01-16.png")
    pixels = list(array.reshape(-1, array.shape[-1]))
    pixels = sorted(pixels, key=lambda x: np.mean(x), reverse=True)
    for idx, rgb in enumerate(pixels):
        y = idx % 800
        x = idx // 800
        py5.stroke(*rgb)
        py5.point(x, y)
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
