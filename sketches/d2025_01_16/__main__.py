"""2025-01-16
Generative palette
Paleta generativa com grade
png
Sketch,py5,CreativeCoding,genuary,genuary2025,genuary16
"""

from random import shuffle

import py5

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    largura = 80
    altura = 80
    grade = cria_grade(py5.width + 100, py5.height + 100, 0, 0, 80, 80, True)
    py5.rect_mode(py5.CENTER)
    py5.stroke("#FFF")
    py5.no_fill()
    shuffle(grade)
    for hb, (xc, yc) in enumerate(grade):
        hb = py5.random_gaussian(int(hb * 1.4))
        with py5.push_matrix():
            py5.translate(xc, yc, 0)
            py5.rotate_y(15)
            for x in range(int(-largura / 2), int(largura / 2), 10):
                s = abs(x) * 1.5 + 20
                py5.rotate_z(15)
                for y in range(int(-altura / 2), int(altura / 2), 10):
                    h = hb + abs(y)
                    b = abs(y) * 1.5 + 20
                    py5.fill(h, s, b)
                    py5.stroke(h, s, b - 10)
                    py5.rect(x, y, 10, 10)
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
