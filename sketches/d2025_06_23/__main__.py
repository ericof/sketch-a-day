"""2025-06-23
Mosaico 04
Mosaico com retângulos em uma grade
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers
from utils.draw import cria_grade_ex

sketch = helpers.info_for_sketch(__file__, __doc__)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.stroke_weight(2)
    py5.stroke(0)
    largura = py5.width * 2
    altura = py5.height * 2
    desv_x = py5.width // 2
    desv_y = py5.height // 2
    cel_x = 28
    cel_y = 7
    grade = cria_grade_ex(largura, altura, 0, 0, cel_x, cel_y, False)
    with py5.push():
        py5.translate(desv_x, desv_y, -10)
        h = py5.random_int(0, 360)
        s = py5.random_int(80, 100)
        b = py5.random_int(30, 90)
        for idx, xb, idy, yb in grade:
            x = xb - desv_x
            y = yb - desv_y
            if py5.random_int(0, 1) == 1:
                h = py5.random_int(0, 360)
                b = py5.random_int(30, 90)
            if idy % 2 == 0:
                dist = int((py5.sqrt(x**2 + y**2) / largura) * 100)
                s = py5.random_int(80 - dist, 100 - dist)
            cor = py5.color(h, s, b)
            py5.fill(cor)
            py5.rect(x, y, cel_x, cel_y)

    helpers.write_legend(sketch=sketch, frame="#000", cor="#fff")


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
