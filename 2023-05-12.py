"""2023-05-12"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from random import shuffle

import numpy as np
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")


def calcula_retangulo(lado_x: int, lado_y: int):
    pontos = []
    step = lado_x * 0.05
    idx = 0
    while idx < lado_x:
        pontos.append((idx, 0))
        pontos.append((0, idx))
        step = step * 1.05
        idx += step
    while idx > 0:
        pontos.append((lado_x, lado_x - idx))
        pontos.append((lado_x - idx, lado_x))
        step = step * 1.05
        idx -= step
    return pontos


def desenha_poligono(pontos, stroke_weight, stroke) -> py5.SHAPE:
    s = py5.create_shape()
    with s.begin_shape():
        py5.stroke(stroke)
        py5.stroke_weight(stroke_weight)
        for x, y in pontos:
            s.vertex(x, y)
    return s


def settings():
    py5.size(WIDTH, HEIGHT)


def setup():
    py5.background(py5.color(248, 241, 219))
    py5.color_mode(py5.HSB, 360, 100, 100, 100)
    py5.no_fill()
    py5.blend_mode(py5.DARKEST)
    y0 = np.arange(-80, HEIGHT + 80, 40)
    x0 = np.arange(-80, WIDTH + 80, 40)
    grade = [(x, y) for x in x0 for y in y0]
    shuffle(grade)
    for x, y in grade:
        lado_x = py5.random_int(40, 80)
        lado_y = py5.random_int(40, 80)
        pontos = calcula_retangulo(lado_x, lado_y)
        cor = py5.color(py5.random_int(0, 360), 100, 100)
        poligono = desenha_poligono(pontos, 2, cor)
        poligono.rotate(py5.radians(py5.random(15, 75)))
        py5.shape(poligono, x, y, lado_x, lado_y)

    write_legend([py5.color(0)], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
