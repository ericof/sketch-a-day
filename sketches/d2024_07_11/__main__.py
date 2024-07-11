"""2024-07-11
Don't Stand so Close To Me '86
Uma singela homenagem ao melhor trio do rock mundial
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(255)
    y0 = 160
    passo = 150
    respiro = 20
    cores = [py5.color(254, 192, 9), py5.color(15, 114, 191), py5.color(220, 29, 10)]
    for cor in cores:
        py5.fill(cor)
        py5.stroke(cor)
        py5.stroke_weight(2)
        for idy in range(passo):
            buffer_x0 = py5.random_int(-40, 40)
            buffer_x1 = py5.random_int(-40, 40)
            py5.line(100 + buffer_x0, y0 + idy, 700 + buffer_x1, y0 + idy)
        y0 += passo + respiro
    py5.stroke(0)
    helpers.write_legend(sketch=sketch, frame="#000")


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
