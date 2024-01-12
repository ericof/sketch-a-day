"""2024-01-13
Genuary 13 - Wobbly function day.
Sequência de curvas sinodais e cossenodais.
png
Sketch,py5,CreativeCoding,genuary,genuary13
"""
from collections import defaultdict

import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

CENTRO = helpers.LARGURA // 2
PONTOS = helpers.LARGURA // 2
X = np.linspace(-CENTRO, CENTRO, PONTOS, True)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.frame_rate(3)


def calcula_pontos(frame, linhas: int = 4):
    anterior = {}
    pontos = defaultdict(list)
    margem = 120
    buffer = np.linspace(0 + margem, py5.width - margem, num=linhas)
    for x in X:
        for linha in range(linhas):
            linha_y = buffer[linha]
            multiplicador = 75 + (linha_y // 100)
            func_1, func_2 = np.sin, np.cos
            if linha % 2:
                func_1, func_2 = func_2, func_1
            y = func_1(
                (3.54 * x)
                + (linha**3)
                - (1.52 * frame)
                + (linha + 2.73)
                + (1.06 * linha) * func_1(1.69 * x - 1.43 * frame + 1.42)
            ) + func_2(
                (3.13 * x)
                - 1.77 * frame
                + (linha + 4.94)
                + ((linha) + 1.21) * func_2(2.10 * x + 1.86 * frame + 4.55)
            ) * multiplicador * func_2(
                x
            )
            x0, y0 = anterior.get(linha_y, (x, y))
            r = linha * 30 + 20
            g = abs(py5.remap(y, -CENTRO, CENTRO, 0, 255))
            b = abs(py5.remap(x, CENTRO, -CENTRO, 255, 0))
            if linha % 2:
                g, b = b, g
            pontos[linha_y].append((x0, y0, x, y, r, g, b))
            anterior[linha_y] = (x, y)
    return pontos


def draw():
    py5.background(248, 241, 219)
    frame = py5.frame_count
    curvas = list(calcula_pontos(frame, 4).items())
    for yb, linha in curvas:
        with py5.push_matrix():
            py5.translate(CENTRO, yb, 0)
            py5.stroke_weight(1)
            for x0, y0, x, y, r, g, b in linha:
                py5.stroke(r, g, b)
                py5.line(x0, y0, x, y)
    helpers.write_legend(sketch=sketch, cor="#000")


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
