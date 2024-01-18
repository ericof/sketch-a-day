"""2024-01-18
Genuary 18 - Bauhaus
Padrão inspirado por Bauhaus, implementado em uma grade de 5 linhas por 5 colunas.
png
Sketch,py5,CreativeCoding,genuary,genuary18
"""
from random import choice

import py5
from numpy.random import choice as np_choice

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)
MARGEM = 50
LARGURA = 140
FUNDO = (30, 30, 30)
CORES = [
    (252, 249, 230),
    (241, 154, 34),
    (25, 103, 160),
    (248, 47, 29),
    (250, 228, 191),
]


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


def modulo_01(x, y, largura, cor, *args):
    x0 = x - largura / 2
    y0 = y - largura / 2
    py5.fill(cor)
    py5.stroke(cor)
    py5.arc(x0, y0, 2 * largura, 2 * largura, py5.radians(0), py5.radians(90))


def modulo_02(x, y, largura, cor, *args):
    x0 = x - largura / 2
    y0 = y - largura / 2
    py5.no_fill()
    py5.stroke_weight(2)
    py5.stroke(cor)
    passos = 12
    passo = largura * 2 / passos
    for i in range(0, passos):
        largura_ = passo * i + passo
        py5.arc(x0, y0, largura_, largura_, py5.radians(0), py5.radians(90))


def modulo_03(x, y, largura, cor_base, cor_alternativa):
    meio = largura / 2
    x0 = x - meio
    y0 = y - meio
    py5.no_fill()
    py5.stroke_weight(2)
    passos = 6
    passo = largura * 2 / passos
    for i in range(passos):
        cor = cor_base if i % 2 else cor_alternativa
        largura_ = passo * i + passo
        py5.stroke(cor)
        py5.arc(x0, y0, largura_, largura_, py5.radians(0), py5.radians(90))


def modulo_04(x, y, largura, cor_base, cor_alternativa):
    meio = largura / 2
    y0 = y - meio
    y1 = y + meio
    py5.rect_mode(py5.CORNERS)
    for x0, x1, cor in ([x - meio, x, cor_base], [x + 1, x + meio, cor_alternativa]):
        py5.fill(cor)
        py5.stroke(cor)
        py5.rect(x0, y0, x1, y1)


def modulo_05(x, y, largura, cor_base, cor_alternativa):
    meio = largura / 2
    quarto = meio / 2
    x0 = x - meio
    x1 = x + meio
    y0 = y - meio
    y1 = y + meio
    py5.rect_mode(py5.CORNERS)
    py5.stroke(cor_base)
    py5.fill(cor_base)
    py5.rect(x0, y0, x1, y1)
    coordenadas = [
        (x0 + quarto, y0 + quarto),
        (x1 - quarto, y0 + quarto),
        (x0 + quarto, y1 - quarto),
        (x1 - quarto, y1 - quarto),
    ]
    for x, y in coordenadas:
        py5.stroke(cor_alternativa)
        py5.fill(cor_alternativa)
        py5.circle(x, y, 10)


MODULOS = [modulo_01, modulo_02, modulo_03, modulo_04, modulo_05]
PROBABILIDADES = [0.4, 0.3, 0.15, 0.05, 0.1]


def borda(xi, xf, yi, yf):
    with py5.push_style():
        py5.rect_mode(py5.CORNERS)
        py5.stroke(0)
        py5.stroke_weight(2)
        py5.no_fill()
        py5.rect(xi - 2, yi - 2, xf + 2, yf + 2)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA)
    py5.frame_rate(1)


def draw():
    py5.background(py5.color(*FUNDO))
    xi = MARGEM
    xf = py5.width - MARGEM
    yi = MARGEM
    yf = py5.height - MARGEM

    pontos = cria_grade(xi, xf, yi, yf, LARGURA, LARGURA, True)
    modulos = [modulo_01, modulo_02, modulo_03, modulo_04, modulo_05]
    for x, y in pontos:
        modulo = np_choice(modulos, 1, p=PROBABILIDADES)[0]
        cor_base = py5.color(*choice(CORES))
        cor_alternativa = py5.color(*choice(CORES))
        if cor_alternativa == cor_base:
            cor_alternativa = py5.color(*choice(CORES))
        rotacao = choice([0, 90, 180, 270])
        with py5.push_matrix():
            py5.translate(x, y)
            py5.rotate(py5.radians(rotacao))
            modulo(0, 0, LARGURA, cor_base, cor_alternativa)
    borda(xi, xf, yi, yf)
    helpers.write_legend(sketch=sketch)
    py5.no_loop()


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()
    elif key == "r":
        py5.redraw()


def save_and_close():
    py5.no_loop()
    helpers.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
