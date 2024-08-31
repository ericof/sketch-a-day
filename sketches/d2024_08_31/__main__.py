"""2024-08-31
Description
Alt
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from copy import deepcopy

import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

MARGEM_X = 0
MARGEM_Y = 0
LARGURA = 80
ALTURA = 80

PALETA = deque(
    [
        "#7ec0e0",
        "#1c8eaf",
        "#032035",
        "#fdaa08",
        "#f87109",
    ]
)


def gera_grade(
    x0: int, y0: int, x1: int, y1: int, n_colunas: int, n_linhas: int
) -> list:
    tam_paleta = len(PALETA)
    altura = int((y1 - y0) / n_linhas)
    largura = int((x1 - x0) / n_colunas)
    y_ = np.linspace(y0, y1, num=n_linhas, endpoint=False)
    x_ = np.linspace(x0, x1, num=n_colunas, endpoint=False)
    grade = []
    for idy, y in enumerate(y_):
        for idx, x in enumerate(x_):
            paleta = deepcopy(PALETA)
            id_cor = (idx + idy) % tam_paleta
            paleta.rotate(-id_cor)
            fundo = paleta.pop()
            pg = py5.create_graphics(largura, altura)
            pg.begin_draw()
            pg.background(fundo)
            for iidx, diametro in enumerate(range(760, 5, -30)):
                pg.stroke(paleta[iidx % (tam_paleta - 1)])
                pg.stroke_weight(30)
                y_c = -y + py5.random_int(-2, 2)
                pg.circle(-x, y_c, diametro)
            pg.end_draw()
            grade.append(((x, y), pg))
    return grade


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.RGB)
    meio_x = py5.width / 2
    meio_y = py5.height / 2
    py5.no_fill()
    py5.blend_mode(py5.BLEND)
    with py5.push_matrix():
        py5.translate(meio_x, meio_y)
        grade = gera_grade(-meio_x, -meio_y, meio_x, meio_y, 10, 10)
        for (x, y), pg in grade:
            py5.image(pg, x, y)
    helpers.write_legend(sketch=sketch)


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
