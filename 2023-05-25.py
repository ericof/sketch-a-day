"""2023-05-25"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import numpy as np
import opensimplex
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")


PONTOS = []


def calcula_circulo(diametro):
    raio = diametro / 2
    n = int(raio)
    pontos = []
    for ponto in range(0, n + 1):
        x = np.cos(2 * py5.PI / n * ponto) * raio
        y = np.sin(2 * py5.PI / n * ponto) * raio
        noise = opensimplex.noise2(x=x, y=y)
        pontos.append((int(x), int(y), noise))
    return pontos


def popula_pontos():
    pontos = []
    step = 20
    diametro = 20
    while diametro < 720:
        pontos.append(calcula_circulo(diametro=diametro))
        if diametro % 180 == 0:
            step += 20
        diametro += step
    return pontos


def desenha_circulo(circulo, idx):
    z = -200 + (idx * 10)
    with py5.begin_shape():
        x0 = None
        y0 = None
        for x, y, noise in circulo:
            h = 80 - (idx * 3)
            s = 100
            b = 100 * abs(noise)
            py5.fill(py5.color(h, s, b))
            py5.stroke(py5.color(h, s, b - 5))
            py5.vertex(x, y, z)
            if x0:
                py5.quadratic_vertex(x0, y0, z, x, y, z)
            x_noise = x + (noise * x / 20)
            y_noise = y + (noise * y / 20)
            py5.quadratic_vertex(x, y, z, x_noise, y_noise, z)
            x_noise_1 = x_noise + (noise * x / 8)
            y_noise_1 = y_noise + (noise * y / 8)
            py5.quadratic_vertex(x_noise, y_noise, z, x_noise_1, y_noise_1, z)
            x0 = x
            y0 = y


def setup():
    global PONTOS
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.frame_rate(5)
    PONTOS = popula_pontos()


def draw():
    py5.background(22, 0, 0)
    write_legend([py5.color(100)], IMG_NAME)
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2, 200)
        for idx, circulo in enumerate(PONTOS[::-1]):
            py5.rotate(py5.radians(py5.random_int(15, 60)))
            desenha_circulo(circulo, idx)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, extension="png")
        py5.exit_sketch()


py5.run_sketch()
