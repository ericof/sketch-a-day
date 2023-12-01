"""2023-12-01"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from random import shuffle

import numpy as np
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")


def circulo(raio, x0=0, y0=0, p=400):
    points = []
    passo = 1 / p
    angulos = np.arange(0, 2 * np.pi, passo)
    for angulo in angulos:
        x = x0 + (raio - (raio * np.cos(angulo)))
        y = y0 + (raio - (raio * np.sin(angulo)))
        points.append((x, y))
    return points


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(py5.color(0))
    py5.stroke(py5.color(360, 0, 100))
    circulo_01 = circulo(100, 400, -400)
    circulo_02 = list(circulo(80, -400, 440))[::-1]
    circulo_ = list(circulo(130, -200, -20))
    shuffle(circulo_)
    CIRCULO = circulo_
    PONTOS = list(zip(circulo_01, circulo_02))
    final = []
    for idx, (p1, p2) in enumerate(PONTOS):
        x0, y0 = CIRCULO[idx]
        p1 = PONTOS[idx][0]
        p2 = PONTOS[idx][1]
        x1 = p1[0] + x0
        y1 = p1[1] + y0
        x2 = p2[0] + x0
        y2 = p2[1] + y0
        x = (x1 + x2) / 2
        y = (y1 + y2) / 4
        final.append((x, y))
    max_x = max([i[0] for i in final])
    min_x = min([i[0] for i in final])
    max_y = max([i[1] for i in final])
    min_y = min([i[1] for i in final])
    with py5.push_matrix():
        py5.translate(WIDTH // 2, HEIGHT // 2, 0)
        for x, y in final:
            h = py5.random_int(0, 360)
            s = py5.random_int(0, 100)
            b = py5.random_int(0, 100)
            raio = py5.random_int(1, 7)
            traco = py5.random_int(1, 2)
            py5.stroke_weight(traco)
            py5.stroke(py5.color(h, s, b))
            py5.circle(x, y, raio)
    write_legend([py5.color(360, 0, 100)], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
