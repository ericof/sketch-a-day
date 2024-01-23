"""2024-01-23
Genuary 23 - 32x32.
Grade de 32 linhas por 32 colunas colorida em gradiente de azul a partir do centro.
png
Sketch,py5,CreativeCoding,genuary,genuary23
"""
from itertools import product

import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

MARGEM = 60
COLUNAS = 32
LINHAS = 32


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CENTER)

    centro = np.array((py5.width / 2, py5.height / 2))
    x0 = MARGEM
    x1 = py5.width - MARGEM
    x = np.linspace(x0, x1, num=COLUNAS, endpoint=True)
    y0 = MARGEM
    y1 = py5.height - MARGEM
    y = np.linspace(y0, y1, num=LINHAS, endpoint=True)
    pontos = product(x, y)
    for coord in pontos:
        dist = np.linalg.norm(np.array(coord) - centro)
        h = py5.remap(dist, 0, 500, 160, 240)
        s = 90
        b = 100
        x, y = coord
        py5.fill(h, s, b)
        py5.stroke(h, s, b)
        py5.square(x, y, 20)
        with py5.push_style():
            s = py5.remap(dist, 0, 500, 100, 40)
            b = py5.remap(dist, 0, 500, 40, 100)
            py5.fill(h, s, b)
            py5.stroke(h, s, b)
            py5.circle(x, y, 10)
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
