"""2023-04-23"""
from helpers import save_image
from helpers import write_legend
from pathlib import Path
import math
import py5

ALTURA = 800
LARGURA = 800

IMG_NAME = Path(__file__).name.replace(".py", "")


PARES = []

ROTACAO = 8


def setup():
    py5.size(LARGURA, ALTURA)
    py5.background(0, 0, 0)
    write_legend(["#FFFFFF"], IMG_NAME)
    # HSB
    py5.frame_rate(20)
    calcula_circulo()
    desenha_circulo()
    desenha_bordas()
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
        total_pares = len(PARES)
        metade = total_pares // 2
        idx = 0
        passo = 1
        for p1, p2 in PARES:
            py5.rotate(py5.radians(ROTACAO))
            linha(p1, p2, idx, metade)
            if idx > metade:
                passo = -1
            idx += passo


def desenha_bordas():
    with py5.push_matrix():
        py5.translate(LARGURA / 2, ALTURA / 2)
        raio = 360
        angulo = 5
        rotacoes = 360 // angulo
        circunferencia = 2 * py5.PI * raio
        segmento = circunferencia / 360 * angulo
        for _ in range(rotacoes):
            py5.rotate(py5.radians(angulo))
            cor = py5.color(
                py5.random(0, 255),
                py5.random(0, 255),
                255,
            )
            triangulo(0, -raio, segmento, cor)


def triangulo(x, y, segmento, cor):
    metade = segmento / 2
    altura = (segmento * math.sqrt(3)) / 2
    py5.fill(cor)
    py5.stroke(cor)
    with py5.begin_shape():
        py5.vertex(x - metade, y)
        py5.vertex(x + metade, y)
        py5.vertex(x, y - altura)
        py5.vertex(x - metade, y)


def linha(p1, p2, idx, metade):
    largura = ((idx % metade) // 20) + 1 if idx < metade else 4
    py5.stroke_weight(largura)
    py5.stroke(idx * 3 + 80, (metade - idx) * 2 + 80, 255)
    py5.no_fill()
    x1, y1 = p1
    x2, y2 = p2
    py5.curve(
        x1 + 80,
        y1 - 80,
        x1,
        y1,
        x2,
        y2,
        x2 - 80,
        y2 + 80,
    )


py5.run_sketch()
