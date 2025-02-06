"""2025-02-06
Hexagons 6
Estudo sobre hexágonos e padrões
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers
from utils.draw import cria_grade_ex, gera_hexagono

sketch = helpers.info_for_sketch(__file__, __doc__)

CELULA_X = helpers.LARGURA / 10
CELULA_Y = CELULA_X * 0.8


PALETA = [
    "#F7D744",
    "#D0341E",
    "#120D2D",
    "#425AC6",
    "#CAC9D1",
]

COR_1 = "#D0341E"
COR_2 = "#120D2D"


def seleciona_cor(idx: int, idy: int) -> str:
    cor = ""
    if idy % 2:
        cor = COR_1 if idx % 3 == 0 else COR_2
    else:
        cor = COR_1 if idx % 3 == 1 else COR_2
    return cor


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(248, 241, 219)
    py5.shape_mode(py5.CENTER)
    grade = cria_grade_ex(py5.width * 4, py5.height * 4, 0, 0, CELULA_X, CELULA_Y, True)
    forma = gera_hexagono()
    forma.set_stroke_weight(3)
    with py5.push_matrix():
        py5.translate(0, -30, -60)
        cor = py5.color(30, 30, 30)
        for idx, x, idy, y in grade:
            cor_base = seleciona_cor(idx, idy)
            for i, diff in enumerate([8, 12]):
                tamanho = CELULA_X - diff
                forma.set_stroke(cor)
                if i:
                    forma.set_fill(py5.color(cor_base))
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
