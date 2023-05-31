"""2023-05-31"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from polygenerator import random_convex_polygon
from random import choice
from random import shuffle

import numpy as np
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

PONTOS = []

DISTANCIA = 20

FORMAS: list[py5.Py5Shape] = []


def cria_forma() -> py5.Py5Shape:
    # Pontos variam entre 0 e 1, multiplicamos os resultados
    # por 50 para fácil "debug"
    num_pontos = py5.random_int(10, 20)
    fator = 50
    forma = py5.create_shape()
    forma.curve_detail(80)
    with forma.begin_closed_shape():
        pontos = [
            (x * fator, y * fator)
            for x, y in random_convex_polygon(num_points=num_pontos)
        ]
        forma.curve_vertex(pontos[0][0], pontos[0][1])
        for x, y in pontos:
            forma.curve_vertex(x, y)
        forma.curve_vertex(x, y)
    return forma


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.frame_rate(1)
    for _ in range(0, 40):
        FORMAS.append(cria_forma())
    x0 = np.arange(DISTANCIA / 2, 2 * WIDTH, DISTANCIA)
    y0 = np.arange(DISTANCIA / 2, 2 * WIDTH, DISTANCIA)
    for x in x0:
        for idy, y in enumerate(y0):
            if idy % 2:
                x = x - DISTANCIA / 2
            if idy % 2:
                y = y - DISTANCIA / 2
            PONTOS.append((x, y))
    shuffle(PONTOS)


def draw():
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(py5.color(220, 50, 100))
    py5.rect_mode(py5.CENTER)
    py5.no_stroke()
    py5.stroke_weight(1)
    tamanho = DISTANCIA * 2.8
    with py5.push_matrix():
        for idx, (x, y) in enumerate(PONTOS):
            forma = choice(FORMAS)
            h = py5.random_int(140, 180)
            s = 100 - (idx % 15)
            color = py5.color(h, s, 100, 80)
            forma.set_stroke_weight(0)
            forma.set_fill(color)
            forma.set_emissive(color)
            forma.rotate(py5.radians(py5.random_int(0, 180)))
            py5.shape(
                forma,
                x,
                y,
                py5.random_int(int(tamanho * 0.3), int(tamanho * 1.8)),
                py5.random_int(int(tamanho * 0.3), int(tamanho * 1.8)),
            )
    write_legend([py5.color(0)], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, extension="png")
        py5.exit_sketch()


py5.run_sketch()
