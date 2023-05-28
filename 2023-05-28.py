"""2023-05-28"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import numpy as np
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")


def retas_ponto(circulo, idx, r_direcao=1):
    duplo = circulo + circulo[1:]
    retas = []
    x0, y0 = circulo[idx]
    pontos_circulo = len(circulo)
    metade = (pontos_circulo / 2) + idx
    resto = metade % 1
    id_min = metade - r_direcao
    id_max = metade + r_direcao
    if resto:
        id_min = id_min + resto
        id_max = id_max - resto
    for id_ponto in range(int(id_min), int(id_max) + 1):
        x1, y1 = duplo[id_ponto]
        retas.append((x0, y0, x1, y1))
    return retas


def calcula_circulo(diametro, n=360):
    raio = diametro / 2
    pontos = []
    for ponto in range(0, n + 1):
        x = np.cos(2 * py5.PI / n * ponto) * raio
        y = np.sin(2 * py5.PI / n * ponto) * raio
        pontos.append((int(x), int(y)))
    return pontos


def setup():
    global PONTOS
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(py5.color(248, 241, 219))
    write_legend([py5.color(0)], IMG_NAME)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CENTER)
    circulos = [
        ((160, 160), 200, 10, 1),
        ((400, 160), 200, 17, 2),
        ((640, 160), 200, 24, 3),
        ((160, 400), 200, 10, 4),
        ((400, 400), 200, 17, 4),
        ((640, 400), 200, 24, 4),
        ((160, 640), 200, 10, 3),
        ((400, 640), 200, 17, 2),
        ((640, 640), 200, 24, 1),
    ]
    for centro, diametro, pontos, r_direcao in circulos:
        circulo = calcula_circulo(diametro, pontos)
        with py5.push_matrix():
            py5.translate(*centro)
            for idx in range(0, len(circulo)):
                retas = retas_ponto(circulo, idx, r_direcao)
                for reta in retas:
                    py5.stroke(350, 0, 0)
                    py5.stroke_weight(1)
                    x0, y0, x1, y1 = reta
                    py5.line(x0, y0, x1, y1)

            py5.stroke(350, 100, 100)
            py5.fill(350, 100, 100)
            for x, y in circulo:
                py5.circle(x, y, 6)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, extension="png")
        py5.exit_sketch()


py5.run_sketch()
