"""2023-07-20"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import numpy as np
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

LINHAS = 8
COLUNAS = 8


def calcula_circulo(diametro):
    pontos = []
    raio = diametro // 2
    n = 360
    for ponto in range(0, n + 1):
        x = np.cos(2 * py5.PI / n * ponto) * raio
        y = np.sin(2 * py5.PI / n * ponto) * raio
        pontos.append((int(x), int(y)))
    return pontos


def poligono(circulo, lados=3):
    angle = 360 / lados
    s = py5.create_shape()
    with s.begin_closed_shape():
        for i in range(0, lados + 1):
            if (idx := int(i * angle)) > 360:
                idx = idx % 360
            x, y = circulo[idx]
            s.vertex(x, y)
    return s


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(py5.color(240, 100, 100))
    largura = WIDTH / COLUNAS
    altura = HEIGHT / LINHAS
    cores_a = [
        [py5.color(240, 50, 50), py5.color(360, 0, 100)],
        [py5.color(360, 0, 100), py5.color(240, 50, 50)],
    ]
    circulo = calcula_circulo(largura)
    forma = poligono(circulo, 6)
    for i in range(LINHAS):
        cores = cores_a[i % 2]
        y = i * altura + altura / 2
        for j in range(COLUNAS):
            cor = cores[j % 2]
            x = j * largura + largura / 2
            forma.set_fill(cor)
            forma.set_stroke(cor)
            py5.shape(forma, x, y, largura, altura)
    write_legend(img_name=IMG_NAME)
    save_image(IMG_NAME, "png")


def key_pressed():
    key = py5.key
    if key == " ":
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
