"""2023-06-30"""
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
    passo = int(TAMANHO / 2 + TAMANHO / 4)
    for y in range(-MARGEM_Y, HEIGHT + MARGEM_Y, passo):
        for x in range(-WIDTH - MARGEM_X, WIDTH + MARGEM_X, TAMANHO):
            PONTOS.append((x, y, forma))
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
    py5.background(FUNDO)
    py5.color_mode(py5.RGB, 255, 255, 255)
    py5.shape_mode(py5.CENTER)
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2)
        r = 90
        g = 0
        b = 250
        for x, y, forma in PONTOS:
            forma.set_stroke(py5.color(255, 255, 255, 50))
            forma.set_fill(py5.color(r, g, b, 100))
            py5.shape(forma, x, y, TAMANHO, TAMANHO)
    write_legend([py5.color(0)], img_name=IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
