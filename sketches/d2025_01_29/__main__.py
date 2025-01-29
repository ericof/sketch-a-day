"""2025-01-29
Grid-based graphic design.
Grade com rosas polares.
png
Sketch,py5,CreativeCoding,genuary,genuary29
"""

import math

import py5

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)


def desenha_rosa(n, d, r, passos, h_base):
    with py5.push_style():
        for i in range(passos):
            angulo = py5.radians(i)
            k = n / d
            x = r * py5.cos(k * angulo) * py5.cos(angulo)
            y = r * py5.cos(k * angulo) * py5.sin(angulo)
            h = h_base + abs((i % 360) - h_base)
            s = 90
            b = 90
            ir = math.sqrt(x**2 + y**2) // 90 + 2
            py5.stroke_weight(ir)
            py5.stroke(h, s - 20, b - 20)
            py5.fill(h, s, b)
            py5.point(x, y)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CENTER)
    celula = 160
    grade = cria_grade(
        int(py5.width * 1.3), int(py5.height * 1.3), -200, -200, celula, celula, False
    )
    for xb, yb in grade:
        xc = xb + celula // 2
        yc = yb + celula // 2
        with py5.push_matrix():
            py5.translate(xc, yc, -20)
            n = 7.6 + py5.random_gaussian(0, 1.1)
            d = py5.random_int(80) / 10
            r = 62
            h_base = py5.random_int(360)
            desenha_rosa(n, d, r, 6000, h_base)
            with py5.push_style():
                py5.stroke_weight(1)
                py5.stroke("#555")
                py5.no_fill()
                for i in range(-4, 4, 3):
                    py5.rect(0, 0, celula + i, celula + i)
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
