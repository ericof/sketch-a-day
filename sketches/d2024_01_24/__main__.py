"""2024-01-24
Genuary 24 - Impossible objects.
Dois Triângulos de Penrose concêntricos.
png
Sketch,py5,CreativeCoding,genuary,genuary24
"""
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def face(lado: int = 100, angulo: int = 0, hb: int = 0):
    passos = [
        (0, lado),
        (120, lado * 5),
        (120, lado * 6),
        (60, lado),
        (120, lado * 5),
        (-120, lado * 3),
    ]
    x = 0
    y = 0
    forma = py5.create_shape()
    with forma.begin_closed_shape():
        for idx, (incremento, tamanho) in enumerate(passos):
            angulo += incremento
            x += py5.cos(py5.radians(angulo)) * tamanho
            y += py5.sin(py5.radians(angulo)) * tamanho
            forma.vertex(x, y)
    for idx in range(forma.get_vertex_count()):
        h = hb + idx * 10
        forma.set_stroke(idx, py5.color(h, 0, 0))
        forma.set_fill(idx, py5.color(h, 80, 100))
    return forma


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P2D)
    py5.background(252, 249, 230)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.shape_mode(py5.CORNER)
    with py5.push_matrix():
        py5.translate(400, 400)
        passos = [
            (50, 225, 0, 38, -18, 5),
            (50, 210, 120, -11, 64, 5),
            (50, 205, 240, -57, -18, 5),
            (10, 125, 0, 0, 2, 2),
            (10, 110, 120, -10, 22, 2),
            (10, 105, 240, -20.0, 2, 2),
        ]
        for lado, h, angulo, x, y, peso in passos:
            py5.stroke_weight(peso)
            forma = face(lado, angulo, h)
            py5.shape(forma, x, y)

    helpers.write_legend(sketch=sketch, cor="#000")


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
