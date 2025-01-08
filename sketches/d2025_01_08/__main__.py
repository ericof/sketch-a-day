"""2025-01-08
One million lines
Desenhando um milhão de linhas
png
Sketch,py5,CreativeCoding,genuary,genuary2025,genuary8
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    with py5.push_matrix():
        py5.translate(py5.width // 2, py5.height // 2, 0)
        for z in range(-60, -40, 2):
            for x in range(-400, 400, 2):
                for y in range(-375, 375, 3):
                    with py5.push_matrix():
                        py5.translate(0, 0, int(py5.random_gaussian(z)))
                        x0 = py5.random_gaussian(x)
                        x0 = x0 if x0 < 400 else 400
                        x1 = py5.random_int(int(x0), 401)
                        h = py5.random_gaussian() * 360
                        s = py5.random_int(40, 90)
                        b = py5.random_int(40, 90)
                        py5.stroke(h, s, b)
                        py5.stroke_weight(py5.random_gaussian(4))
                        py5.line(x0, y, x1, y)
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
