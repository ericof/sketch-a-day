"""2024-11-27
Backlog VII
Grade composta por círculos coloridos
png
Sketch,py5,CreativeCoding
"""

import random

import py5

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)

random.seed(__file__)

MARGEM = 100
CELULA = 20
MEIA_CELULA = CELULA // 2

PALETA = [
    "#F7D744",
    "#D0341E",
    "#D0341E",
    "#120D2D",
    "#425AC6",
    "#CAC9D1",
]


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(py5.random_choice(PALETA))
    py5.rect_mode(py5.CORNERS)
    py5.ellipse_mode(py5.CENTER)
    py5.color_mode(py5.HSB, 360, 100, 100)
    grade = cria_grade(800, 800, MARGEM, MARGEM, CELULA, CELULA, False)
    with py5.push_style():
        for idx, passo in enumerate(range(0, MARGEM)):
            inicio = (MARGEM - 20) + passo
            final = (py5.width - MARGEM + 20) - passo
            py5.fill(py5.random_choice(PALETA))
            py5.rect(inicio, inicio, final, final)
    for x0, y0 in grade:
        x = x0 + MEIA_CELULA
        y = y0 + MEIA_CELULA
        diametro = py5.random_int(MEIA_CELULA, CELULA)
        cor = py5.random_choice(PALETA)
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
