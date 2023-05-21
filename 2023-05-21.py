"""2023-05-21"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

FUNDO = py5.color(248, 241, 219)

MARGEM_X = 200
MARGEM_Y = 200
TAMANHO = 80
TAMANHO_E = 35
PONTOS = []


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.frame_rate(15)
    for idy, y in enumerate(range(-MARGEM_Y, HEIGHT + MARGEM_Y, TAMANHO // 2)):
        buffer_x = 0 if idy % 2 else TAMANHO // 2
        for x in range(-MARGEM_X, WIDTH + MARGEM_X, TAMANHO):
            PONTOS.append((x + buffer_x, y))
    desenha()


def hexagono() -> py5.Py5Shape:
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
    py5.background(FUNDO)
    py5.color_mode(py5.HSB, 100, 100, 100)
    py5.shape_mode(py5.CENTER)
    write_legend([py5.color(0)], img_name=IMG_NAME)
    forma = hexagono()
    for x, y in PONTOS:
        cor = py5.color(abs(y / 9.6), abs(50 - abs(x / 8)), 100, 40)
        forma.set_stroke(py5.color(0))
        forma.set_fill(cor)
        py5.shape(forma, x, y, TAMANHO, TAMANHO)
        cor = py5.color(abs(x / 8), abs(y / 9.6), 100, 80)
        py5.stroke(0)
        py5.fill(cor)
        py5.circle(x, y, TAMANHO_E)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
