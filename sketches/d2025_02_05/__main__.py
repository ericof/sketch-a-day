"""2025-02-05
Hexagons 5
Estudo sobre hexágonos e Mondrian
png
Sketch,py5,CreativeCoding
"""

import numpy as np
import py5

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)

CELULA_X = helpers.LARGURA / 10
CELULA_Y = CELULA_X * 0.8


PALETA = [
    "#F7D744",
    "#D0341E",
    "#D0341E",
    "#120D2D",
    "#425AC6",
    "#CAC9D1",
]


def gera_hexagono() -> py5.Py5Shape:
    pontos = []
    x, y = 0, 0
    largura = 1
    for angle in range(0, 360, 60):
        x += np.cos(py5.radians(angle)) * largura
        y += np.sin(py5.radians(angle)) * largura
        pontos.append((x, y))
    forma = py5.create_shape()
    with forma.begin_closed_shape():
        for x, y in pontos:
            forma.vertex(x, y)
    forma.rotate(py5.radians(30))
    return forma


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(248, 241, 219)
    py5.shape_mode(py5.CENTER)
    grade = cria_grade(py5.width * 4, py5.height * 4, 0, 0, CELULA_X, CELULA_Y, True)
    forma = gera_hexagono()
    forma.set_stroke_weight(5)
    with py5.push_matrix():
        py5.translate(0, -30, -60)
        cor = py5.color(30, 30, 30)
        for x, y in grade:
            for idx, diff in enumerate([8, 16]):
                tamanho = CELULA_X - diff
                forma.set_stroke(cor)
                if idx:
                    forma.set_fill(py5.color(py5.random_choice(PALETA)))
                else:
                    forma.set_fill(py5.color(248, 241, 219))
                py5.shape(forma, x, y, tamanho, tamanho)
    helpers.write_legend(sketch=sketch, cor="#CCC", frame="#333")


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
