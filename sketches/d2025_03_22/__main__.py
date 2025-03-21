"""2025-03-22
Flower
Usando curvas bezier, desenhamos uma sequência de formas que se parecem com flores
png
Sketch,py5,CreativeCoding
"""

from collections import deque

import numpy as np
import py5

from utils import helpers

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
    camadas = [
        [1200, 340, -70, 240, 30, 60],
        [900, 350, -50, 240, 0, 60],
        [750, 0, -45, 240, 30, 60],
        [600, 20, -40, 240, 0, 60],
        [450, 30, -35, 240, 30, 60],
    ]
    for celula, hb, z, angulo, buffer, passo in camadas:
        with py5.push():
            xc = 400
            yc = 400
            py5.translate(xc, yc, z)
            raio = celula / 6
            dist = raio * 2.2
            centro = dist / 2
            for rot in range(0, 360, passo):
                rot += buffer
                with py5.push():
                    py5.rotate(py5.radians(rot))
                    with py5.push():
                        py5.translate(0, -centro)
                        py5.no_fill()
                        py5.stroke_weight(1)
                        desenha_forma(
                            (0, -raio), (0, raio), hb, angulo, dist, num_passos=40
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
