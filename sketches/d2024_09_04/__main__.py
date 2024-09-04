"""2024-09-04
Colorful waves 01
Padrão de ondas coloridas
png
Sketch,py5,CreativeCoding
"""

from collections import deque

import numpy as np
import py5

from utils import helpers

np.logspace
sketch = helpers.info_for_sketch(__file__, __doc__)

PALETA = deque(
    [
        "#7ec0e0",
        "#1c8eaf",
        "#032035",
        "#fdaa08",
        "#f87109",
    ]
)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(252, 249, 230)
    py5.rect_mode(py5.CORNERS)
    py5.stroke_weight(2)
    py5.no_fill()
    passos = 20
    lx = py5.width
    ly = py5.height
    x = np.linspace(0, lx, endpoint=False, num=lx - 0)
    y = np.linspace(10, ly, endpoint=False, num=passos)
    multiplicadores = np.logspace(0.8, 1.6, num=passos // 2, endpoint=False)
    multiplicadores = sorted(multiplicadores) + sorted(multiplicadores, reverse=True)
    pesos = np.linspace(6, 3, num=passos, endpoint=False)
    y = zip(y, multiplicadores, pesos)
    with py5.push_matrix():
        py5.translate(0, 0, -10)
        for yb, mult_b, peso in y:
            y0 = None
            x0 = 0
            py5.stroke_weight(peso)
            for idx, x1 in enumerate(x):
                xd = py5.remap(x1, 0, 800, -60, 60)
                mult = mult_b * py5.cos(py5.radians(xd))
                yd = mult * (
                    abs(py5.cos(py5.radians(x1 + (4 * yb))) * py5.sin(x1) * py5.cos(x0))
                )
                y1 = yb - yd if (idx % 2) else yb + yd
                py5.stroke(PALETA[0])
                if y0 is None:
                    y0 = y1
                py5.line(x0, y0, x1, y1)
                x0, y0 = x1, y1
            PALETA.rotate(1)
    helpers.write_legend(sketch=sketch, frame="#000", cor="#FFF")


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
