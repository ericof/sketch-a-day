"""2023-08-01"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from random import choice
from random import shuffle

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

FUNDO = py5.color(248, 241, 219)

MARGEM_X = WIDTH
MARGEM_Y = HEIGHT
TAMANHO = 60
PONTOS = []


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.frame_rate(15)
    forma = octagono()
    idx = 0
    passo = TAMANHO // 3
    for idy, y in enumerate(range(-MARGEM_Y, HEIGHT + MARGEM_Y, passo)):
        buffer_x = 0 if idy % 2 else TAMANHO // 2
        for x in range(-MARGEM_X, WIDTH + MARGEM_X, passo):
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
    py5.background(FUNDO)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.shape_mode(py5.CENTER)
    total = len(PONTOS)
    fator = 100 / total
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2, 200)
        for angulo in (15,):
            shuffle(PONTOS)
            py5.rotate_y(py5.radians(angulo))
            py5.rotate_z(py5.radians(45))
            for idx, (x, y, forma) in enumerate(PONTOS):
                h = 260
                s = 100
                b = fator * idx
                o = 10
                forma.set_fill(py5.color(h, s, b, o))
                forma.no_fill()
                py5.shape(forma, x, y, TAMANHO, TAMANHO)
    write_legend([py5.color(100)], img_name=IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
