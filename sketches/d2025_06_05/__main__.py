"""2025-06-05
Fraturas Circulares 01
Implementa círculos concêntricos fraturados em pequenos segmentos
png
Sketch,py5,CreativeCoding
"""

from collections import deque

import py5

from utils import helpers
from utils.draw import cria_grade_ex, gera_paleta

sketch = helpers.info_for_sketch(__file__, __doc__)


def gera_grade(
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    n_colunas: int,
    n_linhas: int,
    paleta: list[py5.Py5Color],
) -> list:
    tam_paleta = len(paleta)
    altura = int(y1 - y0)
    largura = int(x1 - x0)
    cel_y = altura // n_linhas
    cel_x = largura // n_colunas
    grade = cria_grade_ex(largura, altura, 0, 0, cel_x, cel_y, False)
    resposta = []
    for idx, xb, idy, yb in grade:
        x = py5.remap(xb, 0, largura, x0, x1)
        y = py5.remap(yb, 0, altura, y0, y1)
        paleta_ = deque([i for i in paleta])
        id_cor = (idx + idy) % tam_paleta
        paleta_.rotate(-id_cor)
        fundo = paleta_.pop()
        pg = py5.create_graphics(largura, altura, py5.P3D)
        with pg.begin_draw():
            pg.background(fundo)
            for iidx, diametro in enumerate(range(760, 5, -30)):
                pg.stroke(paleta_[iidx % (tam_paleta - 1)])
                pg.stroke_weight(30)
                x_c = -x + py5.random_int(-4, 4)
                y_c = -y + py5.random_int(-4, 4)
                pg.circle(x_c, y_c, diametro)
        resposta.append(((x, y), pg))
    return resposta


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    meio_x = py5.width / 2
    meio_y = py5.height / 2
    paleta = gera_paleta("Navy-Orange")
    grade = gera_grade(-meio_x, -meio_y, meio_x, meio_y, 40, 40, paleta)
    with py5.push_matrix():
        py5.translate(meio_x, meio_y)
        for (x, y), pg in grade:
            py5.image(pg, x, y)
    helpers.write_legend(sketch=sketch, frame="#7ec0e0")


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
