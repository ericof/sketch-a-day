"""2023-08-17"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

from random import choice
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

FUNDO = py5.color(0)

PALETA = []


def sorteia_cor(limite=8):
    padrao = py5.color(0)
    valor = py5.random_int(10)
    return padrao if valor < limite else choice(PALETA)


def triangles():
    x = 0
    y = 0
    largura = 70
    metade = largura / 2
    x0 = x
    x1 = x - metade
    x2 = x + metade
    x3 = x2 + metade
    y0 = y
    y1 = y + largura
    s1 = py5.create_shape()
    with s1.begin_shape():
        s1.vertex(x1, y0)
        s1.vertex(x2, y0)
        s1.vertex(x0, y1)
        s1.vertex(x1, y0)

    s2 = py5.create_shape()
    with s2.begin_shape():
        s2.vertex(x0, y1)
        s2.vertex(x3, y1)
        s2.vertex(x2, y0)
        s2.vertex(x0, y1)
    return s1, s2


def setup():
    global PALETA
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(FUNDO)
    py5.color_mode(py5.HSB, 360, 100, 100)
    PALETA = [
        py5.color(115, 147, 126),
        py5.color(120, 190, 150),
        py5.color(206, 185, 146),
        py5.color(30, 80, 150),
        py5.color(70, 90, 20),
        py5.color(71, 19, 35),
        py5.color(88, 85, 99),
        py5.color(91, 46, 72),
    ]
    passo_grid = 80
    forma_1, forma_2 = triangles()
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2)
        py5.rotate(py5.radians(0))
        for base_y in range(-HEIGHT, HEIGHT, passo_grid):
            y = base_y
            for base_x in range(-WIDTH, WIDTH, passo_grid):
                x = base_x
                cor = sorteia_cor(2)
                forma_1.set_stroke_weight(0)
                forma_1.set_stroke(cor)
                cor = sorteia_cor(7)
                forma_1.set_fill(cor)
                py5.shape(forma_1, x, y)
                cor = sorteia_cor(2)
                forma_2.set_stroke_weight(0)
                forma_2.set_stroke(cor)
                cor = sorteia_cor(7)
                forma_2.set_fill(cor)
                py5.shape(forma_2, x + 5, y)

    write_legend([py5.color(360)], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, extension="png")
        py5.exit_sketch()


py5.run_sketch()
