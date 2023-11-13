"""2023-11-05"""
from helpers import CelulaV4 as Celula
from helpers import Grade
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
        x = (np.cos(2 * py5.PI / n * ponto) * raio) + raio
        y = (np.sin(2 * py5.PI / n * ponto) * raio) + raio
        pontos.append((int(x), int(y)))
    return pontos


def poligono(pontos, diametro, lados=3):
    angle = 360 / lados
    s = py5.create_shape()
    with s.begin_closed_shape():
        for i in range(lados, 0 - 1, -1):
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
    diametro = 80
    pontos = calcula_circulo(diametro)
    linhas = 4
    colunas = 4
    margem = 40
    largura = (py5.width - (2 * margem)) / colunas
    grade = Grade(0, 0, WIDTH, HEIGHT, colunas, linhas, margem, margem)
    legendas = []
    for idx, slot in enumerate(grade):
        lados = idx + 4
        linha = idx // colunas
        coluna = idx % colunas
        x, y, largura_celula = slot.x, slot.y, largura
        h = linha * 36
        s = 100 - (coluna * 5)
        b = (coluna * 5) + 10
        cores = [py5.color(h, s, b)]
        forma = poligono(pontos, diametro, lados)
        celula = Celula(
            x,
            y,
            largura_celula,
            [forma],
            cores,
            border=0,
        )
        celula.fill = True
        celula.largura_interna = largura_celula * 0.75
        slot.celulas.append(celula)
        legendas.append((lados, x + largura_celula // 2, y + largura_celula // 2))
    grade.desenha()
    for texto, x, y in legendas:
        py5.fill(py5.color(360, 0, 100))
        py5.text_size(30)
        py5.text_align(py5.CENTER)
        py5.text(texto, x, y)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, extension="png")
        py5.exit_sketch()


py5.run_sketch()