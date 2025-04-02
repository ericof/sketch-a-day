"""2025-04-02
Padrões 02
Padrão de traços em grade
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)

TAMANHO_X = 96
TAMANHO_Y = 96

COR_FUNDO = (42, 42, 165)
COR_TRACO = (80, 164, 96)


def padrao_01(angulo: int = 0) -> py5.Py5Graphics:
    pg = py5.create_graphics(TAMANHO_X, TAMANHO_Y, py5.P3D)
    pg.begin_draw()
    meio_x = TAMANHO_X // 2
    meio_y = TAMANHO_Y // 2
    with pg.push_matrix():
        pg.translate(meio_x, meio_y)
        pg.rotate(angulo)
        pg.background(*COR_FUNDO)
        pg.stroke(*COR_TRACO)
        pg.stroke_weight(2)
        pg.no_fill()
        pg.ellipse_mode(py5.CENTER)
        for d in range(5, TAMANHO_X * 2 - 5, 20):
            pg.circle(meio_x, meio_y, d)
        pg.end_draw()
        pg.rotate(-angulo)
    return pg


def padrao_02(angulo: int = 0) -> py5.Py5Graphics:
    pg = py5.create_graphics(TAMANHO_X, TAMANHO_Y, py5.P3D)
    pg.begin_draw()
    meio_x = TAMANHO_X // 2
    meio_y = TAMANHO_Y // 2
    with pg.push_matrix():
        pg.translate(meio_x, meio_y)
        pg.rotate(angulo)
        pg.background(*COR_FUNDO)
        pg.stroke(*COR_TRACO)
        pg.stroke_weight(2)
        for x in range(-meio_x + 3, meio_x, 10):
            pg.line(x, -meio_y, x, meio_y)
        pg.end_draw()
        pg.rotate(-angulo)
    return pg


def padrao_03(angulo: int = 0) -> py5.Py5Graphics:
    pg = py5.create_graphics(TAMANHO_X, TAMANHO_Y, py5.P3D)
    pg.begin_draw()
    meio_x = TAMANHO_X // 2
    meio_y = TAMANHO_Y // 2
    with pg.push_matrix():
        pg.translate(meio_x, meio_y)
        pg.rotate(angulo)
        pg.background(*COR_FUNDO)
        pg.end_draw()
        pg.rotate(-angulo)
    return pg


PADROES = {1: padrao_01, 2: padrao_02, 3: padrao_03}

GRADE = [
    # Primeira linha
    (1, 0),
    (2, 90),
    (1, 90),
    (1, 0),
    (2, 90),
    (1, 90),
    # Segunda linha
    (2, 0),
    (3, 0),
    (2, 0),
    (2, 0),
    (3, 0),
    (2, 0),
    # Terceira linha
    (1, 270),
    (2, 90),
    (1, 180),
    (1, 270),
    (2, 90),
    (1, 180),
]


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.rect_mode(py5.CORNER)
    idx = 0
    celula = 100
    grade = cria_grade(py5.width, py5.height, 100, 100, celula, celula, False)
    for x, y in grade:
        index = idx % len(GRADE)
        func, graus = GRADE[index]
        padrao = PADROES[func](py5.radians(graus))
        py5.image(padrao, x, y)
        idx += 1
    with py5.push():
        py5.translate(0, 0, -100)
        py5.fill("#000")
        py5.rect(0, 0, py5.width, py5.height)
    helpers.write_legend(sketch=sketch, frame="#000")


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
