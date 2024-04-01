"""2024-04-01
Waves V
Série de ondas, em tons de verde, criadas com funções trigonométricas.
png
Sketch,py5,CreativeCoding,waves
"""

from collections import defaultdict
from typing import List, Tuple

import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

MARGEM = 100


def calcula_circulo(
    largura: int, altura: int, margem: int
) -> List[Tuple[float, float]]:
    """Calcula circulo que toque as margens."""
    raio_x = (largura - (2 * margem)) / 2
    raio_y = (altura - (2 * margem)) / 2
    x0 = margem + raio_x
    y0 = margem + raio_y
    pontos = []
    for angulo in range(0, 360):
        angulo_radianos = py5.radians(angulo)
        x = x0 + (py5.cos(angulo_radianos) * raio_x)
        y = y0 + (py5.sin(angulo_radianos) * raio_y)
        pontos.append((x, y))
    return pontos


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(252, 249, 230)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.no_fill()
    py5.stroke_weight(2)
    circulo = calcula_circulo(py5.width, py5.height, MARGEM)
    pontos_y = defaultdict(set)
    h = 160
    with py5.push_style():
        py5.stroke_weight(6)
        py5.stroke(h, 60, 60)
        for x, y in circulo:
            py5.point(x, y)
            pontos_y[int(y)].add(x)
    limites_y = {k: (min(v), max(v)) for k, v in pontos_y.items()}
    passos = 22
    lx = py5.width - MARGEM
    ly = py5.height - MARGEM
    x = np.linspace(MARGEM, lx, endpoint=False, num=lx - MARGEM)
    y = np.linspace(MARGEM, ly, endpoint=False, num=passos)
    base_multi = np.logspace(0.4, 1.6, num=int(passos / 2), endpoint=False)
    multiplicadores = sorted(base_multi) + sorted(base_multi, reverse=True)
    pesos = np.linspace(4, 2, num=passos, endpoint=False)
    y = zip(y, multiplicadores, pesos)
    for yb, mult_b, peso in y:
        y0 = None
        ybi = int(yb)
        limites = None
        for diff in (0, -1, 1, -2, 2, -3, 3):
            limites = limites_y[ybi + diff] if ybi + diff in limites_y else None
            if limites:
                break
        xi = limites[0]
        x0 = xi
        xf = limites[1]
        py5.stroke_weight(peso)
        s = py5.remap(mult_b, 0, 40, 60, 100)
        for x1 in x:
            if x1 < xi or x1 > xf:
                continue
            xd = py5.remap(x1, 0, 800, -60, 60)
            mult = mult_b * py5.cos(py5.radians(xd))
            y1 = yb + (
                mult * (abs(py5.cos(py5.radians(x0 + (4.1 * yb))) * py5.sin(1.4 * x1)))
            )
            b = py5.remap(xd, -60, 60, 80, 60)
            py5.stroke(h, s, b)
            if y0 is None:
                y0 = y1
            py5.line(x0, y0, x1, y1)
            x0, y0 = x1, y1
    helpers.write_legend(sketch=sketch, cor=py5.color(h, s, b))


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
