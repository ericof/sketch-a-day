"""2026-08-04
BraSil 01
Exercício com as cores da bandeira do Brasil.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.grade import cria_grade_ex
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
paleta = gera_paleta("brasil-03")


def gera_grade(
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    diametro_max: int,
    diametro_min: int,
    n_colunas: int,
    n_linhas: int,
    paleta: list[py5.Py5Color],
) -> list:
    altura = int(y1 - y0)
    largura = int(x1 - x0)
    cel_y = altura // n_linhas
    cel_x = largura // n_colunas
    grade = cria_grade_ex(largura, altura, 2, 2, cel_x, cel_y, False)
    resposta = []
    tam_paleta = len(paleta)
    for idx, xb, idy, yb in grade:
        x = py5.remap(xb, 0, largura, x0, x1)
        y = py5.remap(yb, 0, altura, y0, y1)
        paleta_ = deque(paleta)
        id_cor = (idx + idy) % tam_paleta
        paleta_.rotate(-id_cor)
        pg = py5.create_graphics(largura, altura, py5.P3D)
        pg.rect_mode(py5.CORNER)
        with pg.begin_draw():
            for iidx, diametro in enumerate(range(diametro_max, diametro_min, -3)):
                with pg.push():
                    angulo = -5 if iidx % 2 == 0 else 5
                    pg.rotate(py5.radians(angulo))
                    meio_diametro = diametro / 2
                    pg.stroke(paleta_[iidx % (tam_paleta - 1)])
                    pg.stroke_weight(3)
                    meia_amplitude = idx + idy
                    x0 = (
                        float(-x + py5.random_int(-meia_amplitude, meia_amplitude))
                        - meio_diametro
                    )
                    y0 = (
                        float(-y + py5.random_int(-meia_amplitude, meia_amplitude))
                        - meio_diametro
                    )
                    pg.rect(x0, y0, diametro, diametro)
        resposta.append(((x, y), pg))
    return resposta


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)


def draw():
    py5.background(cor_fundo)
    meio_x = helpers.DIMENSOES.centro[0]
    meio_y = helpers.DIMENSOES.centro[1]
    grade = gera_grade(-meio_x, -meio_y, meio_x, meio_y, 1200, 10, 20, 20, paleta)
    with py5.push_matrix():
        py5.translate(meio_x - 110, meio_y - 120)
        py5.rotate(float(py5.radians(15)))
        for (x, y), pg in grade:
            py5.image(pg, x, y)
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
