"""2025-01-14
Pure black and white
Estática
png
Sketch,py5,CreativeCoding,genuary,genuary2025,genuary14
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

CORES = [
    "#000",
    "#FFF",
]


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    for y in range(0, 801):
        for x in range(0, 801):
            cor = py5.random_choice(CORES)
            py5.stroke(cor)
            py5.point(x, y)
    helpers.write_legend(sketch=sketch, cor="#000", frame="#FFF")


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
