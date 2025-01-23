"""2025-01-23
Hypotrochoid 03 + Gradients
Exercício com equação paramétrica: Hypotrochoid
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.stroke_weight(2)
    R = 13
    r = 5.15
    r_d = R - r
    d = 1.7
    mult = 40
    h = 0
    xa = None
    ya = None
    with py5.push_matrix():
        py5.translate(py5.width / 2, py5.height / 2, -10)
        for i in range(9600):
            angulo = py5.radians(i)
            xb = r_d * py5.cos(angulo) + d * py5.cos((r_d / r) * angulo)
            yb = r_d * py5.sin(angulo) - d * py5.sin((r_d / r) * angulo)
            x = xb * mult
            y = yb * mult
            traco = (abs(x) + abs(y)) / 80
            if (iter := i % 60) == 0:
                h = py5.random_int(0, 360)
            else:
                h += iter
                h = h if h < 360 else h - 360
            s = py5.remap(abs(y) % 200, 0, 400, 80, 100)
            b = py5.remap(abs(x) % 200, 0, 400, 80, 100)
            py5.stroke(h, s, b)
            py5.stroke_weight(traco)
            if not xa:
                py5.point(x, y)
            else:
                py5.line(xa, ya, x, y)
            xa, ya = x, y
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
