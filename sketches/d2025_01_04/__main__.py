"""2025-01-04
Black on Black
Círculos, círculos e mais círculos pretos
png
Sketch,py5,CreativeCoding,genuary,genuary4
"""

from random import shuffle

import py5

from utils import helpers
from utils.draw import pontos_circulo

sketch = helpers.info_for_sketch(__file__, __doc__)

RAIO = 600


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.blend_mode(py5.BLEND)
    py5.stroke_weight(4)
    py5.no_fill()
    for idy, raio in enumerate(range(20, RAIO, 40)):
        total_pontos = idy * 2 + 40
        pontos = pontos_circulo(total_pontos, raio, py5.width // 2, py5.height // 2)
        shuffle(pontos)
        for x, y in pontos:
            with py5.push_matrix():
                py5.translate(x, y, -raio / 20)
                for idx in range(3, 60):
                    c = idx - (idy * 2)
                    py5.stroke(c, c, c)
                    py5.circle(0, 0, idx)

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
