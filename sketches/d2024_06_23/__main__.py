"""2024-06-23
Formas Geométricas 3
Exercício de grade de formas geométricas
png
Sketch,py5,CreativeCoding
"""

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
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.shape_mode(py5.CENTER)
    formas = [hexagono(), octagono()]
    tamanho = 60
    passo = tamanho // 2
    pontos = []
    metade_y = py5.height // 2
    metade_x = py5.width // 2
    for idy, y in enumerate(range(-metade_y - MARGEM_Y, metade_y + MARGEM_Y, passo)):
        buffer_x = 0 if idy % 2 else tamanho // 2
        for idx, x in enumerate(
            range(-metade_x - MARGEM_X, metade_x + MARGEM_X, passo)
        ):
            h = ((py5.sin(py5.radians(2 * idy)) + py5.cos(3 * idx)) * 360) % 360
            forma = formas[idy % 2]
            pontos.append((x + buffer_x, y, forma, h))
            idx += 1
    with py5.push_matrix():
        py5.translate(py5.width / 2, py5.height / 2)
        for angulo in (15,):
            py5.rotate(py5.radians(angulo))
            for idx, (x, y, forma, h) in enumerate(pontos):
                cor = py5.color(h, 80, 80)
                forma.set_stroke_weight(2)
                forma.set_stroke(cor)
                if not (idx % 40):
                    forma.set_fill(cor)
                else:
                    forma.no_fill()
                py5.shape(forma, x, y, tamanho, tamanho)
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
