"""2024-07-06
Dominos
Releitura de sketch_2024_06_04 do Alexandre Villares
png
Sketch,py5,CreativeCoding
"""

from itertools import product

import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def retangulo(info):
    pos, w, h, rot, h = info
    with py5.push_matrix():
        py5.rect_mode(py5.CENTER)
        py5.translate(*pos)
        py5.rotate(rot)
        py5.stroke(h, 80, 100)
        py5.fill(h, 80, 80)
        py5.rect(0, 0, w, h)
    return pos


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    x_a = list(range(-300, 300, 25))
    grade = list(product(x_a, [0] * len(x_a)))
    with py5.push_matrix():
        py5.translate(py5.width / 2, py5.height / 2)
        n = len(grade)
        w = np.linspace(5, 50, n)
        h = np.linspace(-20, 20, n)
        angs = np.linspace(0, py5.PI, n)
        h = np.linspace(120, 200, n)
        retangulos = zip(grade, w, h, angs, h)
        pontos = list(map(retangulo, retangulos))
        py5.points(pontos)
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
