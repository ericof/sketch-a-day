"""2024-01-03
Genuary 03 - Efeito Droste.
Imagem formada por recursivos quadrados.
png
Sketch,py5,CreativeCoding,genuary,genuary3
"""
import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

MARGEM = 80
FUNC = py5.square


def desenho(centro, largura, i=0):
    if i >= 6:
        return
    py5.no_fill()
    x0, y0 = centro
    centro_quadrante = largura // 4
    tamanho_max = largura // 2
    passos = list(np.linspace(start=5, stop=tamanho_max, num=20, endpoint=False))
    quadrantes = (
        (-centro_quadrante, -centro_quadrante),
        (centro_quadrante, -centro_quadrante),
        (-centro_quadrante, centro_quadrante),
        (centro_quadrante, centro_quadrante),
    )
    with py5.push_matrix():
        py5.translate(x0, y0)
        for idy, quadrante in enumerate(quadrantes):
            x, y = quadrante
            if idy == 3:
                py5.stroke(360, 0, 100)
                py5.square(x, y, passos[-1])
                desenho((x, y), passos[-1], i=i + 1)
            else:
                for idx, tamanho in enumerate(passos):
                    h = idx * 10 + (idy * 50)
                    py5.stroke(h, 100, 100)
                    FUNC(x, y, tamanho)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P2D)
    centro = (helpers.LARGURA // 2, helpers.ALTURA // 2)
    py5.background(0)
    py5.rect_mode(py5.CENTER)
    py5.color_mode(py5.HSB, 360, 100, 100)
    desenho(centro, 700)
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
