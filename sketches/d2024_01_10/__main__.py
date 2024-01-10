"""2024-01-10
Genuary 10 - Hexagons
Grade de hexágonos coloridos.
gif
Sketch,py5,CreativeCoding,genuary,genuary10
"""
from random import shuffle

import numpy as np
import py5
import py5_tools

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

CELULA_X = helpers.LARGURA / 12
CELULA_Y = CELULA_X * 0.8
GRADE = None
FORMA = None


def cria_grade_centralizada(celula_x: int, celula_y: int, alternada: bool = True):
    """Cria uma grade com pontos centralizados em cada célula."""
    pontos = []
    celula_x = int(celula_x)
    celula_y = int(celula_y)
    yi = -(celula_y * 2)
    yf = py5.height + (celula_y * 3)
    for idy, y in enumerate(range(yi, yf, celula_y)):
        buffer = int(celula_x / 2) if (alternada and idy % 2) else 0
        xi = -(celula_x * 2) - buffer
        xf = py5.width + (celula_x * 3) + buffer
        for x in range(xi, xf, celula_x):
            pontos.append((x, y))
    return pontos


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
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.shape_mode(py5.CENTER)
    GRADE = cria_grade_centralizada(CELULA_X, CELULA_Y, True)
    shuffle(GRADE)
    FORMA = gera_hexagono()


def draw():
    py5.background(360, 0, 0)
    frame = py5.frame_count
    contador = CELULA_X + frame
    for idx, (x, y) in enumerate(GRADE):
        tamanho = abs(CELULA_X - ((frame + idx + y) % (CELULA_X * 2)))
        h = (contador + idx) % 180 + 100
        s = 100 - tamanho
        b = 80
        FORMA.set_stroke(py5.color(360, 0, 100))
        FORMA.set_stroke_weight(2)
        FORMA.set_fill(py5.color(h, s, b))
        py5.shape(FORMA, x, y, tamanho, tamanho)
    helpers.write_legend(sketch=sketch)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    py5.exit_sketch()


if __name__ == "__main__":
    py5_tools.animated_gif(
        f"{sketch.path}/{sketch.day}.gif",
        count=45,
        period=0.1,
        duration=0.00,
        block=False,
    )
    py5.run_sketch()
