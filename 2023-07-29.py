"""2023-07-29"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import numpy as np
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

FUNDO = py5.color(248, 241, 219)


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


def desenha_poligono(forma, menor, maior, passo, h, x, y, angulo=0):
    for idx, tamanho in enumerate(range(maior, menor, passo)):
        if idx % 3 > 0:
            s = 0
            b = 0
            cor_1 = py5.color(h, s, b)
            s = 100
            b = 40
            cor_2 = py5.color(h, s, b)
        else:
            cor_1 = cor_2 = FUNDO
        forma.set_stroke_weight(1)
        forma.set_stroke(cor_1)
        forma.set_fill(cor_2)
        forma.rotate(py5.radians(angulo))
        py5.shape(forma, x, y, x + tamanho, y + tamanho)


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(FUNDO)
    py5.color_mode(py5.HSB, 360, 100, 100)
    pontos = calcula_circulo(800)
    py5.shape_mode(py5.CORNERS)
    forma = poligono(pontos, 6)
    passo_grid = 160
    buffer = passo_grid / 2
    passo_poligono = -5
    for base_y in range(0, HEIGHT, passo_grid):
        y = base_y + buffer
        for base_x in range(0, WIDTH, passo_grid):
            x = base_x + buffer
            desenha_poligono(
                forma,
                -passo_poligono,
                passo_grid + passo_poligono,
                passo_poligono,
                30,
                x,
                y,
                30,
            )
    write_legend([py5.color(360)], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, extension="png")
        py5.exit_sketch()


py5.run_sketch()
