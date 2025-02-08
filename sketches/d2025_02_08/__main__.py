"""2025-02-08
MSX Lives 02
Outro exemplo de código derivado do MSX1
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)


def estrela(x: int = 0, y: int = 0, r: int = 200, ri: int = 180):
    an = py5.PI * 2 / 5
    a = 0
    forma = py5.create_shape()
    with forma.begin_closed_shape():
        while a < py5.PI * 2 - 0.1:
            x0 = r * py5.cos(a)
            y0 = r * py5.sin(a) * -1
            x2 = ri * py5.cos(a + an / 2)
            y2 = ri * py5.sin(a + an / 2) * -1
            x1 = ri * py5.cos(a - an / 2)
            y1 = ri * py5.sin(a - an / 2) * -1
            forma.vertices(
                [
                    [x1, y1],
                    [x0, y0],
                    [x2, y2],
                ]
            )
            a += an
    return forma


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.shape_mode(py5.CORNER)
    py5.lights()
    py5.stroke_weight(5)
    margem = -py5.width
    celula = 100
    r = celula * 0.8
    grade = cria_grade(
        py5.width * 4, py5.height * 4, margem, margem, celula, celula, True
    )
    for xb, yb in grade:
        x = xb + celula / 2
        y = yb + celula / 2
        h = py5.random_gaussian(180, 100)
        s = py5.random_gaussian(90, 10)
        b = py5.random_gaussian(70, 10)
        angulo = py5.random_gaussian(0, 60)
        ri = r * py5.random_gaussian(0.5, 0.05)
        with py5.push_matrix():
            py5.translate(x, y, -20)
            forma = estrela(0, 0, r, ri)
            forma.set_stroke(py5.color(h, s, b - py5.random_gaussian(0, 12)))
            forma.set_fill(py5.color(h, s, b))
            forma.rotate(angulo)
            py5.shape(forma, 0, 0, r, r)
            with py5.push_style():
                py5.stroke("#000")
                py5.stroke_weight(ri / 3)
                py5.point(0, 0)

    py5.stroke_weight(1)
    helpers.write_legend(sketch=sketch, frame="#504D4D", cor="#F5B316")


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
