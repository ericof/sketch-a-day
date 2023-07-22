"""2023-07-21"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import numpy as np
import py5


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


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(py5.color(0, 0, 0))
    py5.stroke_weight(2)
    diametros = range(50, 850, 50)
    circulos = [calcula_circulo(diametro) for diametro in diametros]
    with py5.push_matrix():
        py5.translate(0, HEIGHT / 2)
        for idx, diametro in enumerate(diametros):
            pontos_1 = circulos[idx]
            buffer_x = diametro / 2
            h = idx * 20
            py5.stroke(py5.color(h, 100, 100))
            s = py5.create_shape()
            s.set_fill(False)
            pontos = pontos_1
            with s.begin_shape():
                for x, y in pontos:
                    s.vertex(x, y)
            py5.shape(s, buffer_x, 0, diametro, diametro)
            py5.shape(s, WIDTH - buffer_x, 0, -diametro, diametro)
    write_legend([py5.color(0, 0, 100)], img_name=IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
