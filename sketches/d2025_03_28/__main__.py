"""2025-03-28
Formas Geométricas 2
Exercício de grade de formas geométricas
png
Sketch,py5,CreativeCoding
"""

from random import choice

import py5

from utils import helpers
from utils.draw import cria_grade_ex

sketch = helpers.info_for_sketch(__file__, __doc__)

MARGEM_X = -300
MARGEM_Y = -300


def octagono() -> py5.Py5Shape:
    s = py5.create_shape()
    with s.begin_closed_shape():
        s.vertex(30, 0)
        s.vertex(60, 0)
        s.vertex(90, 30)
        s.vertex(90, 60)
        s.vertex(60, 90)
        s.vertex(30, 90)
        s.vertex(0, 60)
        s.vertex(0, 30)
    return s


def hexagono() -> py5.Py5Shape:
    s = py5.create_shape()
    with s.begin_closed_shape():
        s.vertex(30, 0)
        s.vertex(60, 0)
        s.vertex(90, 45)
        s.vertex(60, 90)
        s.vertex(30, 90)
        s.vertex(0, 45)
    return s


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.shape_mode(py5.CENTER)
    formas = [hexagono(), octagono()]
    passo = 42
    tamanho = 49
    pontos = []
    angulos = range(0, 360, 8)
    grade = cria_grade_ex(py5.width, py5.height, MARGEM_X, MARGEM_Y, passo, tamanho)
    profundidade = range(-10, 10)
    with py5.push():
        py5.translate(0, 0, -40)
        for idx, x, idy, y in grade:
            buffer_x = 0 if idy % 2 else tamanho // py5.random_gaussian(4, 2)
            buffer_y = 0 if idx % 2 else tamanho // py5.random_gaussian(-4, 2)
            h = (
                py5.random_int(360)
                + (py5.sin(py5.radians(py5.random_int(5) * idx)) * 10)
                - (py5.cos(py5.radians(6 * idy)) * 25)
            )
            s = (py5.sin(py5.radians(3 * idx)) * 135) % 100
            b = (py5.cos(py5.radians(6 * idy)) * 200) % 100
            forma = formas[idy % 2]
            angulo = choice(angulos)
            pontos.append((x + buffer_x, y + buffer_y, forma, h, angulo))
            idx += 1
            for idx, (x, y, forma, h, ang_rot) in enumerate(pontos):
                forma.set_stroke_weight(py5.random_gaussian(4, 2))
                cor = py5.color(h, 0, 0)
                forma.set_stroke(cor)
                cor = py5.color(h, s, b)
                forma.set_fill(cor)
                z = py5.random_choice(profundidade)
                with py5.push_matrix():
                    py5.translate(x, y, z)
                    py5.rotate(py5.radians(ang_rot))
                    py5.shape(forma, 0, 0, tamanho, tamanho)
    helpers.write_legend(sketch=sketch, frame="#000", cor="#FFF")


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
