"""2024-11-03
Memórias 16-bit II
Donut formado por Círculos
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from random import shuffle

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

PALETA = [
    "#032035",
    "#120D2D",
    "#1C8EAF",
    "#425AC6",
    "#7EC0E0",
    "#CAC9D1",
    "#D0341E",
    "#F7D744",
    "#F87109",
    "#FDAA08",
]


def calcula_coordenadas(
    x0: int, y0: int, r: int, passos: int
) -> list[tuple[float, float]]:
    coordenadas = []
    for i in range(passos):
        angulo = (360 / passos) * i
        x = x0 + (py5.cos(py5.radians(angulo)) * r)
        y = y0 + (py5.sin(py5.radians(angulo)) * r)
        coordenadas.append((x, y))
    return coordenadas


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.no_fill()
    shuffle(PALETA)
    paleta = deque(PALETA)
    raio = 200
    passos = 200
    coordenadas = calcula_coordenadas(py5.width / 2, py5.height // 2, raio, passos)
    for idx, (x, y) in enumerate(coordenadas):
        cor = paleta[0]
        traco = (idx % 2 + 1) * 3
        py5.stroke_weight(traco)
        py5.stroke(cor)
        with py5.push_matrix():
            py5.translate(x, y)
            x0 = py5.random_int(-30, 30)
            y0 = py5.random_int(-30, 30)
            py5.circle(x0, y0, raio)
        paleta.rotate(1)
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
