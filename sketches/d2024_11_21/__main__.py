"""2024-11-21
Backlog I
Grade composta por círculos coloridos
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)

MARGEM = 100
CELULA = 20
MEIA_CELULA = CELULA // 2


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background("#032035")
    py5.rect_mode(py5.CORNERS)
    py5.ellipse_mode(py5.CENTER)
    py5.color_mode(py5.HSB, 360, 100, 100)
    grade = cria_grade(800, 800, MARGEM, MARGEM, CELULA, CELULA, False)
    with py5.push_style():
        py5.fill(360, 0, 0)
        py5.rect(60, 60, 740, 740)
    for x0, y0 in grade:
        x = x0 + MEIA_CELULA
        y = y0 + MEIA_CELULA
        diametro = py5.random_int(2, 18)
        h = py5.random_int(0, 360)
        s = py5.random_int(50, 100)
        b = py5.random_int(50, 100)
        cor = py5.color(h, s, b)
        py5.stroke(cor)
        py5.fill(cor)
        py5.circle(x, y, diametro)
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
