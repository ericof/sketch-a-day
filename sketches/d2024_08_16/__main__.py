"""2024-08-16
Hotel 09
Tentativa de recriação de padrão de carpete de um hotel.
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

MARGEM_X = 100
MARGEM_Y = 100
TAMANHO_BLOCO_X = 100
TAMANHO_BLOCO_Y = 100
TAMANHO_X = 96
TAMANHO_Y = 96

FUNDO = (61, 12, 2)
FUNDO_CARPETE = (61, 12, 2)
LINHA_CARPETE = (255, 255, 0)


def fundo() -> py5.Py5Graphics:
    pg = py5.create_graphics(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    pg.begin_draw()
    pg.background(*FUNDO)
    pg.end_draw()
    return pg


def padrao_01(angulo: int = 0) -> py5.Py5Graphics:
    pg = py5.create_graphics(TAMANHO_X, TAMANHO_Y, py5.P3D)
    pg.begin_draw()
    meio_x = TAMANHO_X // 2
    meio_y = TAMANHO_Y // 2
    with pg.push_matrix():
        pg.translate(meio_x, meio_y)
        pg.rotate(angulo)
        pg.background(*FUNDO_CARPETE)
        pg.stroke(*LINHA_CARPETE)
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
        pg.background(*FUNDO_CARPETE)
        pg.stroke(*LINHA_CARPETE)
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
        pg.background(*FUNDO_CARPETE)
        pg.stroke(*LINHA_CARPETE)
        pg.stroke_weight(2)
        pg.no_fill()
        pg.ellipse_mode(py5.CENTER)
        for d in range(5, TAMANHO_X, 20):
            pg.circle(0, 0, d)
        pg.end_draw()
        pg.rotate(-angulo)
    return pg


PADROES = {1: padrao_01, 2: padrao_02, 3: padrao_03}

GRADE = [
    # Primeira linha
    (1, 270),
    (1, 90),
    (3, 0),
    (3, 0),
    (1, 0),
    (1, 180),
    # Segunda linha
    (1, 0),
    (1, 180),
    (1, 0),
    (1, 90),
    (1, 270),
    (1, 90),
]


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    idx = 0
    py5.image(fundo(), 0, 0)
    for y in range(MARGEM_Y, py5.height - MARGEM_Y, TAMANHO_BLOCO_Y):
        for x in range(MARGEM_X, py5.width - MARGEM_X, TAMANHO_BLOCO_Y):
            index = idx % len(GRADE)
            func, graus = GRADE[index]
            padrao = PADROES[func](py5.radians(graus))
            py5.image(padrao, x, y)
            idx += 1
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
