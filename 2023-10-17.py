"""2023-10-17"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")


def forma_01():
    s = py5.create_shape()
    s.set_fill(False)
    s.set_stroke_weight(4)
    with s.begin_shape():
        s.vertex(0, 0)
        s.bezier_vertex(0, 0, 25, 0, 50, 66)
        s.vertex(50, 66)
        s.vertex(50, 200)
        s.vertex(50, 66)
        s.bezier_vertex(50, 66, 75, 0, 100, 0)
        s.vertex(100, 0)
    return s


def forma_02():
    s = py5.create_shape()
    s.set_fill(False)
    s.set_stroke_weight(4)
    with s.begin_shape():
        s.vertex(0, 200)
        s.bezier_vertex(0, 200, 25, 200, 50, 134)
        s.vertex(50, 134)
        s.vertex(50, 0)
        s.vertex(50, 134)
        s.bezier_vertex(50, 134, 75, 200, 100, 200)
        s.vertex(100, 200)
    return s


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    cor_1 = py5.color(220, 179, 190)
    cor_2 = py5.color(210, 180, 190)
    cor_3 = py5.color(255)
    py5.background(py5.color(170, 150, 150))
    py5.shape_mode(py5.CORNER)
    formas = [forma_01(), forma_02()]
    # Grid
    for y in range(0, HEIGHT + 1, 200):
        py5.stroke_weight(4)
        py5.stroke(cor_2)
        py5.line(0, y, WIDTH, y)
        for idx, x in enumerate(range(0, WIDTH + 1, 100)):
            py5.line(x, 0, x, HEIGHT)
            s = formas[idx % 2]
            s.set_stroke(cor_1)
            py5.shape(s, x, y, 100, 200)

    write_legend([cor_3], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
