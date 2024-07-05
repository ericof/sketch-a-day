"""2024-07-05
Manchas 2
Exercício de grade de formas geométricas
png
Sketch,py5,CreativeCoding
"""

from random import choice

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

MARGEM_X = 200
MARGEM_Y = 200


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
    passo = 50
    tamanho = 35
    pontos = []
    angulos = range(0, 360, 12)
    for idy, y in enumerate(range(-MARGEM_Y, py5.height + MARGEM_Y, passo)):
        buffer_x = 0 if idy % 2 else tamanho // 3
        for idx, x in enumerate(range(-MARGEM_X, py5.width + MARGEM_X, passo)):
            buffer_y = 0 if idx % 2 else tamanho // 3
            h = (
                ((idx * idy) % 240)
                + (py5.sin(py5.radians(py5.random_int(5) * idx)) * 10)
                - (py5.cos(py5.radians(6 * idy)) * 25)
            )
            s = (py5.sin(py5.radians(idx ^ 2)) * 200) % 100
            b = (py5.cos(py5.radians(idy)) * 125) % 100
            forma = formas[0] if idx % 7 == 1 else formas[1]
            angulo = choice(angulos)
            pontos.append((x + buffer_x, y + buffer_y, forma, h, angulo))
            idx += 1
        for idx, (x, y, forma, h, ang_rot) in enumerate(pontos):
            forma.set_stroke_weight(5)
            cor = py5.color(h, s, b)
            forma.set_stroke(cor)
            forma.set_fill(cor)
            with py5.push_matrix():
                py5.translate(x, y)
                py5.rotate(py5.radians(ang_rot))
                tamanho_ = tamanho * (py5.random_int(-60, 60) / 100)
                py5.shape(
                    forma,
                    py5.random_int(-30, 30),
                    py5.random_int(-30, 30),
                    tamanho_,
                    tamanho_,
                )
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
