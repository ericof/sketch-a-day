"""2023-04-14"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")


def settings():
    py5.size(WIDTH, HEIGHT)


def setup():
    background()
    write_legend(["#FFFFFF"], IMG_NAME)
    py5.color_mode(py5.HSB)
    bandeirolas()
    save_image(IMG_NAME)


def background():
    py5.background("#000000")


def bandeirolas():
    py5.no_stroke()
    margem = 50
    linhas = 20
    colunas = 20
    lado = (WIDTH - margem * 2) / colunas
    espacamento = 8
    for j in range(linhas):
        for i in range(colunas):
            x = margem + lado / 2 + i * lado
            y = margem + lado / 2 + j * lado
            cor = py5.color(i * 10, j * 20, 200)
            bandeirola(x, y, lado - espacamento, cor)


def bandeirola(x, y, lado, cor):
    min_x = x - (lado / 2)
    min_y = y - (lado / 2)
    max_x = x + (lado / 2)
    max_y = y + (lado / 2)
    med_x = x
    med_y = y + (lado / 4)
    py5.fill(cor)
    with py5.begin_closed_shape():
        py5.vertex(min_x, min_y)
        py5.vertex(max_x, min_y)
        py5.vertex(max_x, max_y)
        py5.vertex(med_x, med_y)
        py5.vertex(min_x, max_y)


py5.run_sketch()
