"""2025-03-21
Petals
Usando curvas bezier, desenhamos uma sequência de formas que se parecem com flores
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
    celula = 100
    grade = cria_grade_ex(py5.width, py5.height, 0, 0, celula, celula, False)
    for idx, xb, idy, yb in grade:
        with py5.push():
            xc = xb + celula / 2
            yc = yb + celula / 2
            py5.translate(xc, yc, -50)
            hb = idy * 20 + idx * 5
            angulo = py5.random_choice(range(180, 270, 10))
            raio = celula / 6
            dist = raio * 2.4
            centro = dist / 2
            passo = py5.random_choice(range(45, 120, 15))
            for rot in range(0, 360, passo):
                with py5.push():
                    py5.rotate(py5.radians(rot))
                    with py5.push():
                        py5.translate(0, -centro)
                        py5.no_fill()
                        py5.stroke_weight(1)
                        desenha_forma(
                            (0, -raio), (0, raio), hb, angulo, dist, num_passos=60
                        )
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
