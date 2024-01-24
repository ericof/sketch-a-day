"""2024-01-25
Genuary 25 - 'I should try to recreate this with code'.
Série de ondas, em tons de azul, criadas com funções trigonométricas.
png
Sketch,py5,CreativeCoding,genuary,genuary25
"""
import numpy as np
import py5

from utils import helpers

np.logspace
sketch = helpers.info_for_sketch(__file__, __doc__)

MARGEM = 100


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(252, 249, 230)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CORNERS)
    py5.stroke_weight(2)
    py5.no_fill()
    passos = 22
    h = 210
    lx = py5.width - MARGEM
    ly = py5.height - MARGEM
    x = np.linspace(MARGEM, lx, endpoint=False, num=lx - MARGEM)
    y = np.linspace(MARGEM, ly, endpoint=False, num=passos)
    multiplicadores = np.logspace(0.4, 1.6, num=passos, endpoint=False)
    pesos = np.linspace(4, 2, num=passos, endpoint=False)
    y = zip(y, multiplicadores, pesos)
    for yb, mult_b, peso in y:
        y0 = None
        x0 = MARGEM
        py5.stroke_weight(peso)
        s = py5.remap(mult_b, 0, 40, 60, 100)
        for x1 in x:
            xd = py5.remap(x1, 0, 800, -60, 60)
            mult = mult_b * py5.cos(py5.radians(xd))
            y1 = yb + (mult * (abs(py5.cos(py5.radians(x0 + (3 * yb))) * py5.sin(x1))))
            b = py5.remap(xd, -60, 60, 80, 60)
            py5.stroke(h, s, b)
            if y0 is None:
                y0 = y1
            py5.line(x0, y0, x1, y1)
            x0, y0 = x1, y1

    for peso, dxi, dyi, dxf, dyf in (
        (5, 0, -10, 0, 0),
        (3, -5, -15, 5, 5),
        (2, -10, -20, 10, 10),
        (1, -15, -25, 15, 15),
    ):
        py5.stroke_weight(peso)
        py5.stroke(h, s, b)
        py5.rect(MARGEM + dxi, MARGEM + dyi, lx + dxf, ly + dyf)
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
