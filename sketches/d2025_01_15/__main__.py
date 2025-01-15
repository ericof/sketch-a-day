"""2025-01-15
Design a rug
Tapete Ikea, como o que tenho na sala
png
Sketch,py5,CreativeCoding,genuary,genuary2025,genuary15
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

FUNDO = (30, 30, 30)

CORES = [
    "#000",
    "#000",
    "#FFF",
    "#FFF",
    "#FFF",
    "#FFF",
    "#FFF",
    "#FFF",
]


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(*FUNDO)
    py5.ellipse_mode(py5.CENTER)
    py5.stroke_weight(1)
    for y in range(30, 771, 4):
        for x in range(200, 601, 4):
            cor = py5.random_choice(CORES)
            py5.stroke(cor)
            py5.fill(cor)
            w = py5.random_gaussian(3)
            h = py5.random_gaussian(3)
            py5.ellipse(x, y, w, h)
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
