"""2025-02-01
Hexagons
Estudo sobre hexágonos
png
Sketch,py5,CreativeCoding
"""

from random import shuffle

import numpy as np
import py5

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)

CELULA_X = helpers.LARGURA / 12
CELULA_Y = CELULA_X * 0.8
GRADE = None
GRADE_HBASE = []
FORMA = None


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
    global FORMA
    global GRADE
    global GRADE_HBASE
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.shape_mode(py5.CENTER)
    GRADE = cria_grade(
        py5.width + 200, py5.height + 200, 0, 0, CELULA_X, CELULA_Y, True
    )
    shuffle(GRADE)
    GRADE_HBASE = [
        abs(py5.random_gaussian((x * idx) % 360, 10))
        for idx, (x, y) in enumerate(GRADE)
    ]
    FORMA = gera_hexagono()


def draw():
    py5.background(360, 0, 0)
    frame = py5.frame_count
    contador = CELULA_X + frame
    with py5.push_matrix():
        py5.translate(0, 0, -40)
        for idx, (x, y) in enumerate(GRADE):
            tamanho = abs(CELULA_X - ((frame + idx + y) % (CELULA_X * 2)))
            h = (GRADE_HBASE[idx] + contador) % 360
            s = 100 - tamanho
            b = 80
            FORMA.set_stroke(py5.color(360, 0, 100))
            FORMA.set_stroke_weight(2)
            FORMA.set_fill(py5.color(h, s, b))
            py5.shape(FORMA, x, y, tamanho, tamanho)
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
