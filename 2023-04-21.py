"""2023-04-21"""
from helpers import save_image
from helpers import write_legend
from pathlib import Path
import math
import py5

ALTURA = 800
LARGURA = 800

IMG_NAME = Path(__file__).name.replace(".py", "")


PONTOS = []


def setup():
    py5.size(LARGURA, ALTURA)
    py5.background(0, 0, 0)
    write_legend(["#FFFFFF"], IMG_NAME)
    # HSB
    py5.frame_rate(20)
    calcula_circulo()
    desenha_circulo()
    save_image(IMG_NAME, "png")


def calcula_circulo():
    diametro = 700
    raio = diametro / 2
    n = 250
    for ponto in range(0, n + 1):
        x = math.cos(2 * py5.PI / n * ponto) * raio
        y = math.sin(2 * py5.PI / n * ponto) * raio
        PONTOS.append((int(x), int(y)))


def desenha_circulo():
    with py5.push_matrix():
        py5.translate(LARGURA / 2, ALTURA / 2)
        for idx in range(0, len(PONTOS) // 2):
            py5.stroke(py5.random(200), py5.random(255), py5.random(200))
            p1 = PONTOS[idx]
            p2 = PONTOS[-idx - 1]
            linha(p1, p2)
    with py5.push_matrix():
        py5.translate(LARGURA / 2, ALTURA / 2)
        py5.rotate(py5.radians(90))
        for idx in range(0, len(PONTOS) // 2):
            py5.stroke(py5.random(200), py5.random(255), py5.random(200))
            p1 = PONTOS[idx]
            p2 = PONTOS[-idx - 1]
            linha(p1, p2)


def linha(p1, p2):
    py5.stroke(py5.random(200), py5.random(255), py5.random(200))
    x1, y1 = p1
    x2, y2 = p2
    py5.line(x1, y1, x2, y2)


py5.run_sketch()
