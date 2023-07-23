"""2023-07-23"""
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
    py5.shape_mode(py5.CORNERS)
    py5.stroke_weight(2)
    diametros = [d for d in range(50, 850, 50)]
    total_diametros = len(diametros)
    circulos = [(diametro, calcula_circulo(diametro)) for diametro in diametros]
    with py5.push_matrix():
        py5.translate(0, HEIGHT / 2)
        for idx in range(total_diametros):
            c_idx = total_diametros - idx - 2
            d_1, c_1 = circulos[idx]
            pontos_1 = sorted([(x, y) for x, y in c_1[180:]], reverse=True)
            if c_idx > -1:
                d_2, c_2 = circulos[c_idx]
                pontos_2 = sorted([(x, y) for x, y in c_2[:181]])
            else:
                pontos_2 = None
            h = 240
            s = 100
            b = 40 + idx * 4
            c = py5.color(h, s, b)
            py5.stroke(c)
            s = py5.create_shape()
            s.set_fill(False)
            with s.begin_shape():
                for x, y in pontos_1:
                    s.vertex(x + d_1 / 2, y)
            py5.shape(s, 0, 0)
            if pontos_2:
                s = py5.create_shape()
                s.set_fill(c)
                with s.begin_shape():
                    for x, y in pontos_2:
                        s.vertex(x + d_2 / 2 + d_1, y)
            py5.shape(s, 0, 0)
    write_legend([py5.color(0, 0, 100)], img_name=IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
