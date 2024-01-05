"""2024-01-05
Genuary 05 - Estilo de Vera Molnár.

png
Sketch,py5,CreativeCoding,genuary,genuary5
"""
import itertools

import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


MARGEM = 50
ITEMS = 10


def quadrilateros(x, y, tamanho, h_base=200, rotacao=0):
    py5.no_fill()
    py5.stroke_weight(2)
    s = 75
    b = 100
    tamanho_max = tamanho * 0.75
    tamanho_min = tamanho * 0.1
    tamanhos = np.linspace(tamanho_min, tamanho_max, num=4, endpoint=True)
    for idx, tamanho in enumerate(tamanhos):
        with py5.push_matrix():
            if idx:
                rot = rotacao
                h = h_base - (idx * 8)
            else:
                rot = -rotacao
                h = h_base + (idx * 8)

            py5.translate(x, y)
            py5.rotate(py5.radians(rot))
            py5.stroke(h, s, b)
            py5.square(0, 0, tamanho)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CENTER)
    largura = py5.width - 2 * MARGEM
    raio = (largura / ITEMS) / 2
    x_a = np.linspace(MARGEM, py5.width - MARGEM, num=ITEMS, endpoint=False)
    y_a = np.linspace(MARGEM, py5.height - MARGEM, num=ITEMS, endpoint=False)
    pontos = list(itertools.product(y_a, x_a))
    total = len(pontos)
    rotacoes = np.logspace(0.001, 1.6, num=total, endpoint=True)
    for index, (y_b, x_b) in enumerate(pontos):
        x = x_b + raio
        y = y_b + raio
        rotacao = rotacoes[index]
        h_base = (y_b / 680) * 360
        quadrilateros(x, y, raio * 2, h_base, rotacao=rotacao)
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
