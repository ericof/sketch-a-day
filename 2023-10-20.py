"""2023-10-20"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from random import shuffle

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

CORES = [
    py5.color(0, 255, 0),
    py5.color(255),
]


def fuji():
    s = py5.create_shape()
    y0 = 120
    with s.begin_shape():
        s.vertex(0, 0)
        s.vertex(800, 0)
        s.vertex(800, 800)
        s.vertex(0, 800)
        s.vertex(0, 0)
        with s.begin_contour():
            s.vertex(1, 799)
            s.vertex(799, 799)
            s.bezier_vertex(799, 799, 550, 400, 475, y0)
            s.vertex(475, y0)
            s.vertex(325, y0)
            s.bezier_vertex(325, y0, 275, 400, 1, 799)
            s.vertex(1, 799)

    return s


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(py5.color(255))
    py5.rect_mode(py5.CORNERS)
    py5.shape_mode(py5.CORNERS)
    x0 = 80
    x1 = WIDTH - x0
    y0 = 420
    y1 = HEIGHT - 80
    cor_traco = py5.color(188, 0, 45)
    py5.no_stroke()
    py5.fill(cor_traco)
    py5.circle(WIDTH // 2, HEIGHT // 2, 300)
    cor_ceu = py5.color(29, 91, 188)
    cor_monte = py5.color(238, 240, 241)
    py5.stroke(cor_traco)
    py5.fill(cor_monte)
    py5.stroke_weight(8)
    py5.rect(x0, y0, x1, y1)
    s = fuji()
    s.set_stroke_weight(5)
    s.set_fill(cor_ceu)
    py5.shape(s, x0, y0, x1, y1)
    write_legend([py5.color(0)], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
