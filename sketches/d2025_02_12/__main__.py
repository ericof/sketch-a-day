"""2025-02-12
Geometric art redux 02
Grade com paralelogramas
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers
from utils.draw import cria_grade_ex

sketch = helpers.info_for_sketch(__file__, __doc__)


def paralelograma(largura: float, altura: float, altura_interna: float) -> py5.Py5Shape:
    forma = py5.create_shape()
    x0 = x3 = y0 = 0
    x1 = x2 = largura
    y1 = altura - altura_interna
    y2 = altura
    y3 = altura_interna
    vertices = [
        [x0, y0],
        [x1, y1],
        [x2, y2],
        [x3, y3],
    ]
    with forma.begin_closed_shape():
        forma.vertices(vertices)
    return forma


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.shape_mode(py5.CORNER)
    x_m = py5.width / 2
    y_m = py5.height / 2
    lg = 60
    al = 80
    grade = cria_grade_ex(
        4 * py5.width, 4 * py5.height, -py5.width, -py5.height, lg, al, False
    )
    forma = paralelograma(lg, al, al / 2)
    forma.set_stroke_weight(4)
    with py5.push_matrix():
        py5.translate(x_m, y_m, -60)
        for idx, x, _, y in grade:
            x -= x_m
            y -= y_m
            direcao_x = -1 if idx % 2 else 1
            largura = lg * direcao_x
            altura = al
            x0 = lg if direcao_x == -1 else 0
            y0 = al
            h = py5.random_gaussian(220, 50)
            s = py5.random_gaussian(75, 10)
            b = py5.random_gaussian(80, 10)
            forma.set_stroke(py5.color(h, s, b - 10))
            forma.set_fill(py5.color(h, s, b))
            with py5.push_matrix():
                py5.translate(x, y, 0)
                py5.shape(forma, x0, y0, largura, altura)
                py5.translate(0, 0, -2)
                py5.shape(forma, x0 + 1, y0, largura, altura)

    helpers.write_legend(sketch=sketch, frame="#000", cor="#fff")


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
