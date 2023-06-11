"""2023-06-11"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import numpy as np
import py5


SIZE = 80
IMG_NAME = Path(__file__).name.replace(".py", "")


def calcula_circulo(diametro):
    pontos = []
    raio = diametro // 2
    n = 360
    for ponto in range(0, n + 1):
        x = np.cos(2 * py5.PI / n * ponto) * raio
        y = np.sin(2 * py5.PI / n * ponto) * raio
        pontos.append((int(x), int(y)))
    return pontos


def poligono(pontos, lados=3):
    angle = 360 / lados
    s = py5.create_shape()
    with s.begin_closed_shape():
        for i in range(0, lados + 1):
            if (idx := int(i * angle)) > 360:
                idx = idx % 360
            x, y = pontos[idx]
            s.vertex(x, y)
    return s


def setup():
    py5.size(WIDTH, HEIGHT, py5.P2D)
    py5.background(py5.color(248, 241, 219))
    write_legend([py5.color(0)], IMG_NAME)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.shape_mode(py5.CENTER)
    pontos = calcula_circulo(50)
    tamanho = SIZE - 20
    for idy, y in enumerate(range(SIZE + 30, HEIGHT, SIZE)):
        lados = idy + 3
        forma = poligono(pontos, lados)
        h = idy * 36
        s = 0
        b = 0
        cor = py5.color(h, s, b)
        forma.set_stroke(cor)
        forma.set_stroke_weight(2)
        for idx, x in enumerate(range(-10, WIDTH, SIZE)):
            s = 100 - (idx * 5)
            b = (idx * 5) + 10
            cor = py5.color(h, s, b)
            forma.set_fill(cor)
            forma.rotate(py5.radians(idx * 45))
            py5.shape(forma, x, y, tamanho, tamanho)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, extension="png")
        py5.exit_sketch()


py5.run_sketch()
