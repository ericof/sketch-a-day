"""2024-01-17
Genuary 17 - Inspired by Islamic art.
Padrão hexagonal feito em tons pastéis.
png
Sketch,py5,CreativeCoding,genuary,genuary17
"""
import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

MARGEM = 40


def cria_grade(
    xi: int,
    xf: int,
    yi: int,
    yf: int,
    celula_x: int,
    celula_y: int,
    centralizada: bool = False,
):
    """Cria uma grade."""
    pontos = []
    celula_x = int(celula_x)
    celula_y = int(celula_y)
    metade_x = celula_x / 2
    metade_y = celula_y / 2
    for yb in range(yi, yf, celula_y):
        y = yb + (metade_y if centralizada else 0)
        for xb in range(xi, xf, celula_x):
            x = xb + (metade_x if centralizada else 0)
            pontos.append((x, y))
    return pontos


def circulo():
    pontos = []
    for angle in range(0, 360):
        x = np.cos(py5.radians(angle))
        y = np.sin(py5.radians(angle))
        pontos.append((x, y))
    return pontos


CIRCULO = circulo()


def gera_hexagono(xc, yc, largura):
    pontos = []
    inclinacao = 30
    for idx in range(0, 6):
        angulo = ((idx * 60) + inclinacao) % 360
        x, y = CIRCULO[angulo]
        x = xc + (x * largura)
        y = yc + (y * largura)
        pontos.append((x, y))
    return pontos


def desenha_hexagono(xc, yc, largura, nivel, h_base):
    stroke_weight = 6 - nivel
    h = py5.remap(nivel, 0, 10, h_base, h_base + 120)
    s = 70 + nivel * 2
    b = 60
    o = 100 - (nivel * 12)
    forma = py5.create_shape()
    pontos = gera_hexagono(0, 0, largura)
    with forma.begin_closed_shape():
        for x, y in pontos:
            forma.vertex(x, y)
    with py5.push_style():
        forma.set_fill(py5.color(h, s, b, o))
        forma.set_stroke(py5.color(h, s, b + 5))
        forma.set_stroke_weight(stroke_weight)
        py5.shape_mode(py5.CORNER)
        py5.shape(forma, xc, yc, largura, largura)


def forma(raio, niveis: int = 6, h_base: int = 40):
    distancia = raio / niveis
    for nivel in range(niveis):
        tamanho = distancia / ((nivel + 1) * 0.15)
        dist = distancia * nivel
        total = nivel * 6 if nivel else 1
        for idx in range(total):
            angulo = int(idx * (360 / total))
            x, y = CIRCULO[angulo]
            x = x * dist
            y = y * dist
            desenha_hexagono(x, y, tamanho, nivel, h_base)


def borda(cor):
    with py5.push_style():
        py5.no_stroke()
        py5.fill(cor)
        py5.rect_mode(py5.CORNER)
        py5.rect(0, 0, py5.width, MARGEM)
        py5.rect(0, 0, MARGEM, py5.height)
        py5.rect(py5.width - MARGEM, 0, py5.width, py5.height)
        py5.rect(0, py5.height - MARGEM, py5.width, py5.height)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P2D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    xi = MARGEM
    xf = py5.width - MARGEM
    yi = MARGEM
    yf = py5.height - MARGEM
    largura = 240
    pontos = cria_grade(xi, py5.width, yi, py5.height, largura, largura, False)
    py5.rect_mode(py5.CENTER)
    for x, y in pontos:
        with py5.push_matrix():
            py5.translate(x, y)
            forma(largura / 2, niveis=3, h_base=210)
    pontos = cria_grade(xi, xf, yi, yf, largura, largura, True)
    py5.rect_mode(py5.CENTER)
    for x, y in pontos:
        with py5.push_matrix():
            py5.translate(x, y)
            forma(largura / 2, niveis=4, h_base=200)
    borda(py5.color(0, 20, 20, 20))
    helpers.write_legend(sketch=sketch)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    helpers.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
