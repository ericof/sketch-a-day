"""2024-08-09
Hotel 02
Tentativa de recriação de padrão de carpete de um hotel.
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

TAMANHO_X = 96
TAMANHO_Y = 96


def padrao_01(angulo: int = 0) -> py5.Py5Graphics:
    pg = py5.create_graphics(TAMANHO_X, TAMANHO_Y, py5.P3D)
    pg.begin_draw()
    with pg.push_matrix():
        pg.translate(TAMANHO_X / 2, TAMANHO_Y / 2)
        pg.rotate(angulo)
        pg.background(165, 42, 42)
        pg.stroke(255, 255, 255)
        pg.stroke_weight(2)
        pg.no_fill()
        pg.ellipse_mode(py5.CENTER)
        for d in range(5, TAMANHO_X * 2 - 5, 20):
            pg.circle(TAMANHO_X / 2, TAMANHO_Y / 2, d)
        pg.end_draw()
    return pg


def padrao_02(angulo: int = 0) -> py5.Py5Graphics:
    pg = py5.create_graphics(TAMANHO_X, TAMANHO_Y, py5.P3D)
    pg.begin_draw()
    meio_x = TAMANHO_X // 2
    meio_y = TAMANHO_Y // 2
    with pg.push_matrix():
        pg.translate(meio_x, meio_y)
        pg.rotate(angulo)
        pg.background(165, 42, 42)
        pg.stroke(255, 255, 255)
        pg.stroke_weight(2)
        pg.ellipse_mode(py5.CENTER)
        for d in range(-meio_x + 50, meio_y - 50, 50):
            x = helpers.LARGURA - d
            pg.line(x, 0, x, helpers.ALTURA)
        pg.end_draw()
    return pg


PADROES = {1: padrao_01, 2: padrao_02}

GRADE = [
    (1, 0),
    (2, 0),
    (1, 90),
]


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0, 0, 0)
    for idy, y in enumerate(range(100, py5.height - 100, 100)):
        for idx, x in enumerate(range(100, py5.width - 100, 100)):
            index = (idy + idx) % len(GRADE)
            func, graus = GRADE[index]
            padrao = PADROES[func](py5.radians(graus))
            py5.image(padrao, x, y)
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
