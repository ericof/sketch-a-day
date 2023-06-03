"""2023-06-03"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from random import shuffle

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

FUNDO = py5.color(248, 241, 219)

MARGEM_X = 600
MARGEM_Y = 600
TAMANHO = 80
PONTOS = []


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.frame_rate(15)
    for idy, y in enumerate(range(-MARGEM_Y, HEIGHT + MARGEM_Y, TAMANHO // 4)):
        buffer_x = 0 if idy % 2 else TAMANHO // 2
        for x in range(-MARGEM_X, WIDTH + MARGEM_X, TAMANHO):
            PONTOS.append((x + buffer_x, y))
    shuffle(PONTOS)
    desenha()


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


def desenha():
    py5.background(FUNDO)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.shape_mode(py5.CENTER)
    total = len(PONTOS)
    fator = 100 / total
    forma = hexagono()
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2)
        for angulo in range(0, 15, 15):
            py5.rotate(py5.radians(angulo))
            for idx, (x, y) in enumerate(PONTOS):
                h = angulo
                s = idx * fator
                b = 100 - s
                forma.set_fill(py5.color(h, s, b, 40))
                forma.set_stroke_weight(2)
                py5.shape(forma, x, y, TAMANHO, TAMANHO)
    write_legend([py5.color(100)], img_name=IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
