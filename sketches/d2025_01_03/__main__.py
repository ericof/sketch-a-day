"""2025-01-03
The Answer (in 42 lines of code, including comments)
6 x 9 = 42
png
Sketch,py5,CreativeCoding,genuary,genuary3
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(252, 249, 230)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.fill(0)
    s0, p0, p1 = 246, 200, 600
    py5.rect(p0 - 30, p0 - 30, p1 - p0 + 60, p1 - p0 + 60)
    helpers.write_legend(sketch=sketch, frame="#000")
    py5.blend_mode(py5.SCREEN)
    py5.no_fill()
    py5.stroke_weight(12)
    for idy in range(9):
        y = s0 + (idy * 40)
        h, s, b = (180 - idy * 4, 80, 70) if idy < 7 else (80, 60, 60)
        py5.stroke(h, s, b)
        py5.line(p0, y, p1, y)
    for idx in range(6):
        x = s0 + (idx * 60)
        h, s, b = (280 - idx * 6), 80, 70
        py5.stroke(h, s, b)
        py5.line(x, p0, x, p1)
    helpers.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
