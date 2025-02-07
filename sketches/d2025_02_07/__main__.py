"""2025-02-07
MSX Lives 01
Reescrita de código compartilhado por Neilton Pereira.
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    xr = 70
    yr = 64
    cx = 400
    cy = 400
    mult = 3
    py5.stroke_weight(4)
    for sc in range(0, 60, 2):
        for angulo in range(0, 1440):
            x = cx + (
                (xr + sc * py5.sin(py5.radians(10 * angulo)))
                * py5.cos(py5.radians(angulo))
                * mult
            )
            y = cy + (
                (yr + sc * py5.sin(py5.radians(7 * angulo)))
                * py5.sin(py5.radians(angulo))
                * mult
            )
            h = abs(py5.random_gaussian(sc * 6, 10))
            s = py5.remap(angulo, 0, 1440, 80, 100)
            b = py5.remap(sc + angulo, 0, 1500, 80, 100)
            py5.stroke(h, s, b)
            py5.point(x, y)
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
