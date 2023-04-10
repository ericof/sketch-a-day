"""2023-04-07"""
from random import choice
from py5 import *
from pathlib import Path


FOLDER = Path(__file__).parent.resolve()
IMG_FOLDER = FOLDER / 'images'


paleta_base = [
    color(0, 255, 0),
    color(0, 255, 200),
    color(100, 255, 80),
    color(140, 235, 73),
    color(50, 255, 99),
    color(75, 255, 200),
]

paleta_diversa = [
    # Red, Green, Blue
    color(255, 0, 0),
    color(200, 0, 0),
    color(150, 0, 0),
    color(200, 0, 200),
    color(150, 0, 255),
    color(100, 0, 255),
    color(50, 0, 255),
    color(102, 0, 255),
]


def settings():
    size(800, 800)


def fundo():
    for i in range(0, 801):
        if i % 2:
            stroke(i / 4, 0, i)
        else:
            stroke(0, i / 4, i)
        line(0, i, 800, i)


def par_bagunca(faixa_bagunca):
    bx = random(-faixa_bagunca, faixa_bagunca)
    by = random(-faixa_bagunca, faixa_bagunca)
    return bx, by


def quadrado_molnar(x, y, lado, faixa_bagunca, preencher):
    bx, by = par_bagunca(faixa_bagunca)
    x0, y0 = x - lado / 2 + bx, y - lado / 2 + by
    bx, by = par_bagunca(faixa_bagunca)
    x1, y1 = x + lado / 2 + bx, y - lado / 2 + by
    bx, by = par_bagunca(faixa_bagunca)
    x2, y2 = x + lado / 2 + bx, y + lado / 2 + by
    bx, by = par_bagunca(faixa_bagunca)
    x3, y3 = x - lado / 2 + bx, y + lado / 2 + by
    if preencher:
        no_stroke()
        fill(preencher)
    else:
        no_fill()
        stroke(color(0,0,0))
    quad(x0, y0, x1, y1, x2, y2, x3, y3)


def elementos(x, y, lado, idx_linha, idx_coluna):
    # Tamanho do novo elemento
    lado_interno = lado - 10

    # Escolhe cor de preenchimento
    if int(random(400)) == 0:
        preenchimento = choice(paleta_diversa)
    else:
        preenchimento = choice(paleta_base)

    # Primeiro elemento é preenchido
    bagunca = lado_interno * (idx_linha / 85)
    quadrado_molnar(x, y, lado_interno, bagunca, preenchimento)
    # Segundo elemento é apenas a linha
    bagunca = lado_interno * (idx_coluna / 150)
    quadrado_molnar(x, y, lado_interno, bagunca, None)


def setup():
    fundo()
    rect_mode(CENTER)
    colunas = 20
    linhas = 20
    margem = 50
    w = (800 - margem * 2) / colunas
    for j in range(linhas):
        for i in range(colunas):
            x = margem + w / 2 + i * w
            y = margem + w / 2 + j * w
            elementos(x, y, w, j, i)
    img = get(0, 0, 800, 800)
    img.save(IMG_FOLDER / "2023-04-07.jpg")

run_sketch()
