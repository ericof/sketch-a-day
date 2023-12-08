"""2023-12-08"""
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


def espiral(raio, x0=0, y0=0, passos=10, voltas=5, direcao=1):
    points = []
    x_ = []
    y_ = []
    for theta in np.linspace(0, 2 * np.pi * voltas, passos):
        r = theta**2
        x_.append(r * np.cos(theta))
        y_.append(r * np.sin(theta))
    min_x, max_x = min(x_), max(x_)
    min_y, max_y = min(y_), max(y_)
    for x, y in zip(x_, y_):
        x = py5.remap(x, min_x, max_x, x0 - raio, x0 + raio)
        y = py5.remap(y, min_y, max_y, y0 - raio, y0 + raio)
        if direcao:
            points.append((x, y))
        else:
            points.append((y, x))
    return points


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(py5.color(0))
    py5.stroke(py5.color(360, 0, 100))
    r2 = 50
    circulo_int = list(circulo(r2, 10, 10, 800))
    shuffle(circulo_int)
    total_pontos = len(circulo_int)
    r1 = 800
    for rotacao, voltas, direcao in ((0, 10, 0), (0, 11, 1), (90, 10, 0), (90, 11, 1)):
        espiral_ = espiral(r1, 0, 0, passos=total_pontos, voltas=10, direcao=direcao)
        margem = 5
        with py5.push_matrix():
            py5.translate(WIDTH // 2, HEIGHT // 2, -40)
            py5.rotate(py5.radians(rotacao))
            for idx, (x0, y0) in enumerate(espiral_):
                x1_, y1_ = circulo_int[idx]
                x1 = py5.remap(x1_, 0, r2 * 2, x0 - margem, x0 + margem)
                y1 = py5.remap(y1_, 0, r2 * 2, y0 - margem, y0 + margem)
                h = py5.random_int(0, 360)
                s = py5.random_int(60, 100)
                b = py5.random_int(60, 100)
                py5.stroke(py5.color(h, s, b))
                py5.fill(py5.color(h, b, s))
                py5.circle(x1, y1, py5.random_int(1, 6))
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
