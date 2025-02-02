"""2025-02-02
Hexagons 2
Estudo sobre hexágonos e paleta de cor
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
    py5.background(248, 241, 219)
    frame = py5.frame_count
    total = len(PALETA)
    with py5.push_matrix():
        py5.translate(0, 0, -40)
        for idx, (x, y) in enumerate(GRADE):
            tamanho = abs(CELULA_X - ((frame + idx + y) % (CELULA_X * 2)))
            FORMA.set_stroke(py5.color(50, 50, 50))
            FORMA.set_stroke_weight(2)
            cor_idx = idx % total
            cor = py5.color(*PALETA[cor_idx])
            FORMA.set_fill(cor)
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
