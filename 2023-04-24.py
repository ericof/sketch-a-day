"""2023-04-24"""
from helpers import save_image
from helpers import write_legend
from pathlib import Path
import math
import py5

ALTURA = 800
LARGURA = 800

IMG_NAME = Path(__file__).name.replace(".py", "")


PARES = []

ROTACAO = [9, 115, 115, 9]


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
    pontos = []
    pares = []
    for ponto in range(0, n + 1):
        x = math.cos(2 * py5.PI / n * ponto) * raio
        y = math.sin(2 * py5.PI / n * ponto) * raio
        pontos.append((int(x), int(y)))
    for idx in range(len(pontos) // 2):
        pares.append((pontos[idx], pontos[-idx - 1]))
    pares.sort()
    PARES.extend(pares)


def desenha_circulo():
    with py5.push_matrix():
        py5.translate(LARGURA / 2, ALTURA / 2)
        py5.stroke_weight(3)
        py5.stroke(0, 0, 0)
        py5.fill(10, 10, 10)
        py5.circle(0, 0, 700)
        total_pares = len(PARES)
        metade = total_pares // 2
        idx = 0
        passo = 1
        for i, (p1, p2) in enumerate(PARES):
            py5.rotate(py5.radians(ROTACAO[i % 4]))
            linha(p1, p2, idx, metade)
            if idx > metade:
                passo = -1
            idx += passo


def linha(p1, p2, idx, metade):
    largura = ((idx % metade) // 20) + 1 if idx < metade else 4
    py5.stroke_weight(largura)
    py5.stroke(idx * 3 + 40, (metade - idx) * 4 + 20, 200)
    x1, y1 = p1
    x2, y2 = p2
    py5.line(
        x1,
        y1,
        x2,
        y2,
    )


py5.run_sketch()
