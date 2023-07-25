"""2023-07-25"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import numpy as np
import py5


SIZE = 780
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
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(py5.color(248, 241, 219))
    write_legend([py5.color(0)], IMG_NAME)
    py5.color_mode(py5.HSB, 360, 100, 100)
    pontos = calcula_circulo(800)
    tamanho = SIZE
    py5.shape_mode(py5.CORNERS)
    with py5.push_matrix():
        py5.translate(WIDTH // 2, HEIGHT // 2)
        for lados in range(10, 2, -1):
            forma = poligono(pontos, lados)
            h = lados * 36
            s = 0
            b = 0
            cor = py5.color(h, s, b)
            forma.set_stroke(cor)
            forma.set_stroke_weight(5)
            s = 100
            b = 40
            cor = py5.color(h, s, b)
            forma.set_fill(cor)
            py5.shape(forma, 0, 0, tamanho, tamanho)
            print(lados, tamanho)
            tamanho = tamanho * 0.8


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, extension="png")
        py5.exit_sketch()


py5.run_sketch()
