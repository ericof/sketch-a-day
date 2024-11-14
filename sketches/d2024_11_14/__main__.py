"""2024-11-14
Memórias 16-bit XIII
Interferências
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from random import shuffle

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

PALETA = [
    "#7ec0e0",
    "#1c8eaf",
    "#032035",
    "#fdaa08",
    "#f87109",
]


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.no_fill()
    shuffle(PALETA)
    paleta = deque(PALETA)
    py5.ellipse_mode(py5.CORNER)
    py5.rect_mode(py5.CORNER)
    py5.no_fill()
    meio_w = py5.width / 2
    meio_h = py5.height / 2
    for angulo in range(0, 361, 15):
        with py5.push_matrix():
            py5.translate(meio_w, meio_h)
            py5.rotate(py5.radians(angulo))
            for idx, raio in enumerate(range(300, 600, 20)):
                diametro_x = raio * py5.random(1.2, 1.6)
                diametro_y = raio * py5.random(1.2, 1.4)
                cor = paleta[idx % 2]
                py5.stroke_weight((idx % 4) + 4)
                py5.stroke(cor)
                py5.ellipse(-meio_w, -meio_h - raio, diametro_x, diametro_y)
                paleta.rotate(1)
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
