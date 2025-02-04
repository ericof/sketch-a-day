"""2025-02-04
Hexagons 4
Estudo sobre hexágonos
png
Sketch,py5,CreativeCoding
"""

import numpy as np
import py5

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)

CELULA_X = helpers.LARGURA / 12
CELULA_Y = CELULA_X * 0.8
PALETA = [
    (0, 0, 0),
    (127, 143, 110),
    (179, 176, 133),
    (200, 200, 200),
    (212, 198, 170),
    (218, 211, 189),
    (90, 119, 168),
    (187, 137, 30),
    (30, 30, 30),
    (40, 50, 60),
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
        forma.no_fill()
        for x, y in pontos:
            forma.vertex(x, y)
    forma.rotate(py5.radians(15))
    return forma


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(248, 241, 219)
    py5.shape_mode(py5.CENTER)
    py5.lights()
    grade_x = 4 * py5.width
    grade_y = 4 * py5.height
    meio_x = py5.width // 2
    meio_y = py5.width // 2
    grade = cria_grade(grade_x, grade_y, 0, 0, CELULA_X, CELULA_Y, True)
    forma = gera_hexagono()
    forma.set_stroke_weight(5)
    for z in range(-400, 0, 80):
        with py5.push_matrix():
            py5.translate(meio_x, meio_y, z)
            cor = py5.color(*py5.random_choice(PALETA))
            for xb, yb in grade:
                x = xb - grade_x // 2
                y = yb - grade_y // 2
                tamanho = CELULA_X
                forma.set_stroke(cor)
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
