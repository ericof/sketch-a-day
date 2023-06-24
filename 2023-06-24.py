"""2023-06-24"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5

IMG_NAME = Path(__file__).name.replace(".py", "")


FUNDO = py5.color(0, 0, 0)

MARGEM_X = 700
MARGEM_Y = 700
TAMANHO = 50
PONTOS = []


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    forma = octagono()
    idx = 0
    passo = TAMANHO // 2
    for idy, y in enumerate(range(-MARGEM_Y, HEIGHT + MARGEM_Y, passo)):
        buffer_x = 0 if idy % 2 else TAMANHO // 2
        for x in range(-WIDTH - MARGEM_X, WIDTH + MARGEM_X, TAMANHO):
            PONTOS.append((x + buffer_x, y, forma))
            idx += 1
    desenha()


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


def desenha():
    py5.color_mode(py5.RGB, 255, 255, 255)
    py5.shape_mode(py5.CENTER)
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2)
        o = 40
        x_offset = 0
        for angulo in (0, 30, 60):
            r = py5.random_int(0, 255)
            g = py5.random_int(0, 255)
            b = py5.random_int(0, 255)
            o += angulo / 2
            x_offset += angulo
            py5.rotate(py5.radians(angulo))
            for x, y, forma in PONTOS:
                forma.set_stroke(py5.color(255, 255, 255, 5))
                forma.set_fill(py5.color(r, g, b, o))
                py5.shape(forma, x + x_offset, y, TAMANHO, TAMANHO)
    write_legend([py5.color(100)], img_name=IMG_NAME)
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
