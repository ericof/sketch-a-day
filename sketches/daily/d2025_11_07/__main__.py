"""2025-11-07
Noise lines 01
Exercício de criação de linhas com ruído e paleta de cores.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color("#000")
    py5.background(cor_fundo)
    paleta: deque[py5.Py5Color] = gera_paleta("mondrian", True)
    passos = 180
    lx = py5.width
    ly = py5.height // 2
    x = np.linspace(-lx, lx, endpoint=False, num=py5.width * 2)
    y = np.linspace(-ly + 50, ly, endpoint=True, num=passos)
    multiplicadores = np.logspace(0.9, 2.0, num=passos // 2, endpoint=False)
    multiplicadores = sorted(multiplicadores) + sorted(multiplicadores, reverse=True)
    pesos = np.linspace(5, 1, num=passos, endpoint=False)
    y = zip(y, multiplicadores, pesos, strict=True)
    with py5.push():
        py5.rect_mode(py5.CORNERS)
        py5.stroke_weight(1)
        py5.no_fill()
        py5.translate(lx, ly, -40)
        for yb, mult_b, peso in y:
            y0 = None
            x0 = 0
            py5.stroke_weight(peso)
            for idx, x1 in enumerate(x):
                xd = py5.remap(x1, -lx, lx, -40, 40)
                mult = mult_b * py5.cos(py5.radians(xd))
                yd = mult * (
                    abs(py5.cos(py5.radians(x1 + (3 * yb))) * py5.sin(x1) * py5.cos(x0))
                )
                y1 = yb - yd if (idx % 2) else yb + yd
                py5.stroke(paleta[0])
                if y0 is None:
                    y0 = y1
                py5.line(x0, y0, x1, y1)
                x0, y0 = x1, y1
            paleta.rotate(1)
    # Credits and go
    canvas.sketch_frame(
        sketch, cor_fundo, "large_transparent_white", "transparent_white"
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
