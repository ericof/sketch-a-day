"""2025-04-03
Padrões 03
Padrão de traços em grade com paleta inspirada em Warhol
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers
from utils.draw import cria_grade, gera_paleta

sketch = helpers.info_for_sketch(__file__, __doc__)

TAMANHO_X = 96
TAMANHO_Y = 96


def padrao_01(pg: py5.Py5Graphics, meio_x: float, meio_y: float) -> None:
    pg.stroke_weight(2)
    pg.no_fill()
    pg.ellipse_mode(py5.CENTER)
    for d in range(5, TAMANHO_X * 2 - 5, 20):
        pg.circle(meio_x, meio_y, d)


def padrao_02(pg: py5.Py5Graphics, meio_x: float, meio_y: float) -> None:
    pg.stroke_weight(2)
    for x in range(-meio_x + 3, meio_x, 10):
        pg.line(x, -meio_y, x, meio_y)


def padrao_03(pg: py5.Py5Graphics, meio_x: float, meio_y: float) -> None:
    return


def desenha_padrao(
    padrao_id: int, angulo: int, cor_fundo: py5.Py5Color, cor_traco: py5.Py5Color
) -> py5.Py5Graphics:
    pg = py5.create_graphics(TAMANHO_X, TAMANHO_Y, py5.P3D)
    func = globals()[f"padrao_{padrao_id:02d}"]
    with pg.begin_draw():
        meio_x = TAMANHO_X // 2
        meio_y = TAMANHO_Y // 2
        with pg.push_matrix():
            pg.translate(meio_x, meio_y)
            pg.rotate(angulo)
            pg.background(cor_fundo)
            pg.stroke(cor_traco)
            func(pg, meio_x, meio_y)
            pg.rotate(-angulo)
    return pg


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
    paleta = gera_paleta("Warhol", True)
    for x, y in grade:
        index = idx % len(GRADE)
        padrao_id, graus = GRADE[index]
        cor_fundo = paleta[0]
        cor_traco = paleta[1]
        padrao = desenha_padrao(padrao_id, py5.radians(graus), cor_fundo, cor_traco)
        py5.image(padrao, x, y)
        idx += 1
        paleta.rotate(2)
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
