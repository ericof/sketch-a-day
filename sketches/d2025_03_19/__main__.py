"""2025-03-19
Onions
Usando curvas bezier, desenhamos uma sequência de formas que se parecem com cebolas
png
Sketch,py5,CreativeCoding
"""

from collections import deque

import numpy as np
import py5

from utils import helpers
from utils.draw import cria_grade_ex

sketch = helpers.info_for_sketch(__file__, __doc__)


def _bezier_meio(
    p0: np.array,
    p1: np.array,
    distance: float,
    v_rotated,
):
    return p0 + distance * v_rotated


def calcula_passo(
    hb: int, maxima: float, diff: float
) -> tuple[float, float, py5.Py5Color]:
    distancia = maxima - diff
    larg = (diff / maxima) * 2
    h = hb
    s = 90 - (diff / maxima)
    b = 100 - (diff / maxima)
    cor = py5.color(h, s, b)
    return distancia, larg, cor


def desenha_forma(
    p0: tuple[float, float],
    p1: tuple[float, float],
    hb: float,
    angulo: float,
    distancia_max: float,
    num_passos: int = 5,
):
    angle_rad = np.radians(angulo / 2)
    x0, y0 = p0
    x1, y1 = p1
    p0 = np.array(p0)
    p1 = np.array(p1)
    v = p1 - p0
    v = v / np.linalg.norm(v)

    rotacoes = deque(
        [
            np.dot(
                np.array(
                    [
                        [np.cos(angle_rad), -np.sin(angle_rad)],
                        [np.sin(angle_rad), np.cos(angle_rad)],
                    ]
                ),
                v,
            ),
            np.dot(
                np.array(
                    [
                        [np.cos(-angle_rad), -np.sin(-angle_rad)],
                        [np.sin(-angle_rad), np.cos(-angle_rad)],
                    ]
                ),
                v,
            ),
        ]
    )
    distancia_min = distancia_max * 0.1
    passos = [
        calcula_passo(hb, distancia_max, i)
        for i in np.geomspace(distancia_min, distancia_max, num_passos, False)
    ]
    for distancia, largura, cor in passos:
        with py5.push():
            py5.stroke(cor)
            py5.stroke_weight(largura)
            with py5.begin_shape():
                for rotacao in rotacoes:
                    py5.vertex(x0, y0)
                    x_, y_ = _bezier_meio(p0, p1, distancia, rotacao)
                    py5.bezier_vertex(x0, y0, x_, y_, x1, y1)
                    py5.vertex(x1, y1)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    celula_x = 140
    celula_y = 140
    meio_x = celula_x / 2
    meio_y = celula_y / 2
    buffer = 0
    hb = 15
    for idx, xb, idy, yb in cria_grade_ex(
        py5.width * 2,
        py5.height * 2,
        margem_x=-200,
        margem_y=-200,
        celula_x=celula_x,
        celula_y=celula_y,
        alternada=True,
    ):
        x = xb + meio_x
        y = yb + meio_y
        angulo = 90
        if idy % 2:
            p0 = (0, -meio_y - buffer)
            p1 = (0, meio_y + buffer)
            hb = py5.random_gaussian(15, 20)
        else:
            p0 = (0, meio_y + buffer)
            p1 = (0, -meio_y - buffer)
        if idx % 2:
            hb += 5
        with py5.push():
            py5.translate(x, y, -50)
            py5.no_fill()
            py5.stroke_weight(1)
            desenha_forma(p0, p1, hb, angulo, celula_x, num_passos=40)
    helpers.write_legend(sketch=sketch, frame="#CC0022", cor="#FFF")


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
