"""2026-01-29
Waves 03
Desenho de ondas com variações baseadas em funções trigonométricas e logarítmicas.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color(0)
    py5.background("#222222")
    with py5.push():
        paleta = gera_paleta("laranja-01", True)
        py5.no_fill()
        passos = 90
        lx = helpers.DIMENSOES.internal[0] // 2
        ly = helpers.DIMENSOES.internal[1] // 2
        x = np.linspace(-lx, lx, endpoint=False, num=helpers.DIMENSOES.internal[0])
        y = np.linspace(-ly, ly + 40, endpoint=True, num=passos)
        multiplicadores = np.logspace(0.9, 1.7, num=passos // 2, endpoint=False)
        multiplicadores = sorted(multiplicadores) + sorted(
            multiplicadores, reverse=True
        )
        pesos = np.linspace(1.3, 2.1, num=passos // 2, endpoint=False)
        pesos = sorted(pesos) + sorted(pesos, reverse=True)
        y = zip(y, multiplicadores, pesos, strict=False)
        with py5.push():
            py5.translate(*helpers.DIMENSOES.centro, -10)
            for idy, (yb, mult_b, peso) in enumerate(y):
                y0 = None
                x0 = 0
                for idx, x1 in enumerate(x):
                    xd = py5.remap(x1, -lx, lx, -200, 220)
                    mult = mult_b * py5.cos(py5.radians(xd))
                    yd = mult * (
                        abs(
                            py5.cos(py5.radians(x0 + (2 * yb)))
                            * py5.cos(py5.radians(x1 + yb))
                            * py5.sin(py5.radians(idy))
                        )
                    )
                    y1 = yb + yd if (idx % 2) else yb - yd

                    if y0 is None:
                        y0 = y1
                    if peso > 1.3:
                        py5.stroke(paleta[0])
                        py5.stroke_weight(peso)
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
