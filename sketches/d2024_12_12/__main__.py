"""2024-12-12
Formas Geométricas 1
Exercício de grade de formas geométricas
png
Sketch,py5,CreativeCoding
"""

from random import choice

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

MARGEM_X = 100
MARGEM_Y = 100


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
    passo = 30
    tamanho = 45
    pontos = []
    angulos = range(0, 180, 3)
    with py5.push_matrix():
        py5.translate(0, 0, -20)
        for idy, y in enumerate(range(-MARGEM_Y, py5.height + MARGEM_Y, passo)):
            buffer_x = 0 if idy % 2 else tamanho // 2
            for idx, x in enumerate(range(-MARGEM_X, py5.width + MARGEM_X, passo)):
                h = ((py5.sin(py5.radians(2 * idy)) + py5.cos(3 * idx)) * 360) % 360
                forma = formas[idy % 2]
                angulo = choice(angulos)
                pontos.append((x + buffer_x, y, forma, h, angulo))
                idx += 1
            for idx, (x, y, forma, h, ang_rot) in enumerate(pontos):
                forma.set_stroke_weight(2)
                cor = py5.color(h, 0, 0)
                forma.set_stroke(cor)
                cor = py5.color(h, 50, 70)
                forma.set_fill(cor)
                with py5.push_matrix():
                    py5.translate(x, y)
                    py5.rotate(py5.radians(ang_rot))
                    py5.shape(forma, 0, 0, tamanho, tamanho)
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
