"""2024-12-19
49 Anos / 49 Years
Celebrando meus 49 anos, de maneira simples
png
Sketch,py5,CreativeCoding,Birthday
"""

import py5

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)


LARGURA = 100
ALTURA = 100


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    margem_x = 50
    margem_y = 50
    grade = cria_grade(
        py5.width, py5.height, margem_x, margem_y, LARGURA, ALTURA, False
    )
    for idx, (x0, y0) in enumerate(grade, 1):
        h = int(idx * 4.081)
        s = 100 - idx
        b = 40
        py5.stroke_weight(3)
        py5.stroke(h, s, b)
        py5.fill(h, s, b)
        py5.square(x0, y0, LARGURA - 8)
        py5.stroke_weight(1)
        h = int(idx * 4.081)
        py5.stroke(h, s, b)
        s = 50
        b = 80
        py5.fill(h, s, b)
        x = x0 + LARGURA / 2
        y = y0 + ALTURA / 2
        py5.circle(x, y, idx)

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
