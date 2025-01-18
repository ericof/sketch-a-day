"""2025-01-18
What does wind look like?
Exercício com tons de cinza
png
Sketch,py5,CreativeCoding,genuary,genuary2025,genuary18
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

MARGEM = -120


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.stroke_weight(1)
    x0 = MARGEM
    xf = py5.height - MARGEM
    with py5.push_matrix():
        py5.translate(0, 0, MARGEM)
        for y0 in range(MARGEM, py5.height - MARGEM, 32):
            xb = x0
            yb = y0
            mult_b = py5.random_gaussian(8, 2)
            mult_h = py5.random_gaussian(10, 6)
            shift = py5.random_gaussian(py5.width // 2, 100)
            g = py5.remap(shift, 0, py5.width, 100, 255)
            for x in range(x0, xf):
                mult = mult_b if py5.random_gaussian(100, 80) % 8 == 1 else mult_h
                y = y0 + (py5.cos(x + shift) * mult) + (py5.sin(x - shift) * mult)
                py5.stroke(g, g, g)
                py5.line(xb, yb, x, y)
                yb = y
                xb = x
    py5.stroke("#000")
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
