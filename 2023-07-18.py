"""2023-07-18"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import numpy as np
import py5

IMG_NAME = Path(__file__).name.replace(".py", "")

PONTOS = []

POL_1 = None
POL_2 = None


def calcula_circulo(diametro):
    pontos = []
    raio = diametro // 2
    n = 360
    for ponto in range(0, n + 1):
        x = np.cos(2 * py5.PI / n * ponto) * raio
        y = np.sin(2 * py5.PI / n * ponto) * raio
        pontos.append((int(x), int(y)))
    return pontos


def sorteia_cores():
    h1 = 210
    h2 = 30
    s = py5.random(22, 90)
    b = py5.random(50, 75)
    return (py5.color(h2, s, b), py5.color(h1, s, b + 10))


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
    global POL_1, POL_2
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    buffer = 1
    largura = HEIGHT // 10
    linhas = HEIGHT + (buffer * largura) // largura
    colunas = HEIGHT + (buffer * largura) // largura
    buffer_linha = 0
    circulo = calcula_circulo(50)
    POL_1 = poligono(circulo, 6)
    POL_2 = poligono(circulo, 4)
    for i in range(linhas):
        y = i * largura - buffer_linha
        buffer_coluna = 0
        for j in range(colunas):
            x = j * largura - buffer_coluna
            PONTOS.append((x, y, largura))
    print(f"Finalizado Setup com {linhas} {colunas}")
    desenha(POL_1, POL_2)


def desenha(forma1, forma2):
    forma2.rotate(py5.radians(45))
    total_pontos = len(PONTOS)
    py5.shape_mode(py5.CENTER)
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2)
        py5.rotate(py5.radians(0))
        print(f"{total_pontos}")
        for idx, (base_x, base_y, largura) in enumerate(PONTOS):
            if idx % 100 == 0:
                print(f"  - {(idx / total_pontos) * 100}")
            x = base_x - WIDTH
            y = base_y - HEIGHT
            cor1, cor2 = sorteia_cores()
            if idx % 2 == 1:
                cor1, cor2 = cor2, cor1
            # Desenha poligono externo
            forma2.set_fill(cor1)
            py5.shape(forma2, x, y, largura, largura)
            # Desenha poligono interno
            largura_interno = largura * 0.75
            forma1.set_fill(cor2)
            py5.shape(forma1, x, y, largura_interno, largura_interno)
    write_legend(img_name=IMG_NAME)
    save_image(IMG_NAME, "png")


def key_pressed():
    key = py5.key
    if key == " ":
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
