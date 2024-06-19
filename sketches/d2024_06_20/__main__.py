"""2024-06-20
Espiral Redux 13
Exercício de espirais criadas a partir de uma espiral central
png
Sketch,py5,CreativeCoding,espirais
"""

import math
from random import choice, shuffle

import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def calcular_espiral(
    x0: int,
    y0: int,
    offset: int,
    n_pontos: int,
    raio_max: int,
    escala: float = 0.1,
    crescimento: float = 0.0,
) -> list[tuple[float, float, float]]:
    pontos: list[tuple[float, float, float]] = []
    crescimento = crescimento if crescimento else raio_max / n_pontos

    t = np.linspace(0, 5 * np.pi, n_pontos)
    x_a = x0 + (escala + crescimento * t) * np.cos(t + offset)
    y_a = y0 + (escala + crescimento * t) * np.sin(t + offset)
    for i in range(n_pontos):
        x = x_a[i]
        y = y_a[i]
        r = math.sqrt((x - x0) ** 2 + (y - y0) ** 2)
        pontos.append((x, y, r))
    return pontos


def desenha_espiral(
    x0: float,
    y0: float,
    offset: float,
    cores: list[int] | None = None,
    idx: int = 1,
    n_pontos: int = 200,
    raio_max: int = 600,
):
    escala = py5.random(0.05, 0.5)
    crescimento = py5.random(3, 5)
    pontos = calcular_espiral(
        x0, y0, offset, n_pontos, raio_max, escala=escala, crescimento=crescimento
    )
    for idx, (x, y, r) in enumerate(pontos):
        multiplicador = py5.sin(py5.radians(r + 0.5 * idx)) + py5.cos(
            py5.radians(idx) + (0.2 * r)
        )
        h = choice(cores) + (py5.random_int(2, 4) * multiplicador)
        s = py5.random_int(50, 60) + (1 * multiplicador * py5.sin(idx))
        b = py5.random_int(60, 80) + (0.8 * multiplicador * py5.cos(idx))
        py5.stroke(h, s, b)
        py5.fill(h, s, b)
        func = py5.square if idx % 2 == 1 else py5.circle
        func(x, y, 2 * multiplicador)


def espirais(
    x: float,
    y: float,
    cores: list[int] | None = None,
    n_pontos: int = 50,
    raio_max: int = 200,
):
    total_cores = len(cores)
    offset = 360 / total_cores
    angulo = py5.random_int(360)
    desenha_espiral(x, y, angulo, cores, idx=0, n_pontos=n_pontos, raio_max=raio_max)
    angulo -= offset


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(360, 0, 0)
    pontos = calcular_espiral(400, 400, 0, 100, 800, escala=-5, crescimento=40)
    for x, y, r in pontos:
        cores = list(range(0, 360, 5))
        shuffle(cores)
        espirais(x, y, cores)
    helpers.write_legend(sketch=sketch, frame="#000")


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
