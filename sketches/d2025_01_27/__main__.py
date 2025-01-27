"""2025-01-27
Rose 01
Polar Rose
png
Sketch,py5,CreativeCoding
"""

import math

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.blend_mode(py5.DIFFERENCE)
    n = 4.2
    d = 5.5
    r = 400
    with py5.push_matrix():
        py5.translate(py5.width / 2, py5.height / 2, -30)
        for i in range(9600):
            angulo = py5.radians(i)
            k = n / d
            x = r * py5.cos(k * angulo) * py5.cos(angulo)
            y = r * py5.cos(k * angulo) * py5.sin(angulo)
            h = 180 + abs((i % 360) - 180)
            s = 90
            b = 90
            ir = math.sqrt(x**2 + y**2) // 40 + 2
            py5.stroke_weight(ir - 4)
            py5.stroke(h, s - 20, b - 20)
            py5.fill(h, s, b)
            py5.circle(x, y, ir)
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
