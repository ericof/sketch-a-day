"""2023-12-03"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from random import shuffle

import numpy as np
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")


def circulo(raio, x0=0, y0=0, p=900):
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
    r1 = 250
    circulo_ = circulo(r1, 0, 0)
    r2 = 50
    circulo_int = list(circulo(r2, 10, 10))
    shuffle(circulo_int)
    with py5.push_matrix():
        py5.translate(WIDTH // 2, HEIGHT // 2, 0)
        for idx, (x_, y_) in enumerate(circulo_):
            x0 = py5.remap(x_, 0, r1 * 2, -200, 200)
            y0 = py5.remap(y_, 0, r1 * 2, 150, -150)
            x1_, y1_ = circulo_int[idx]
            x1 = py5.remap(x1_, 0, r2 * 2, -30, 30)
            y1 = py5.remap(y1_, 0, r2 * 2, -30, 30)
            x, y = (x0 + x1), (y0 + y1)
            h = py5.random_int(0, 360)
            s = py5.random_int(0, 100)
            b = py5.random_int(0, 100)
            py5.stroke(py5.color(h, s, b))
            py5.point(x0, y0)
            h = py5.random_int(0, 360)
            py5.fill(py5.color(h, b, s))
            py5.circle(x, y, py5.random_int(1, 4))
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
