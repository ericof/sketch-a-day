"""2024-06-16
Espiral Redux 9
Criação de espirais formadas por quadrados
png
Sketch,py5,CreativeCoding,grid
"""

from random import shuffle

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def espiral(x0: float, y0: float, offset: float, h_base: float = 40, idx: int = 1):
    pontos = 200
    raio_max = 600
    for i in range(pontos):
        angulo = py5.radians((idx + i) * 5 - offset)
        r = i * py5.sin(i**2) * raio_max / pontos
        x = x0 + r * py5.cos(angulo * idx)
        y = y0 + r * py5.sin(angulo * idx)
        multiplicador = py5.sin(py5.radians(r + 0.5 * i)) + py5.cos(
            py5.radians(i) + (0.2 * r)
        )
        h = h_base + (3 * multiplicador)
        s = 50 + (1 * multiplicador * py5.sin(angulo))
        b = 80 + (0.8 * multiplicador * py5.cos(angulo))
        py5.stroke(h, s, b)
        py5.fill(h, s, b)
        func = py5.square if i % 7 == 1 else py5.circle
        func(x, y, 2 * multiplicador)


def espirais(x: float, y: float, cores: list[int] | None = None):
    total_cores = len(cores)
    offset = 360 / total_cores
    angulo = py5.random_int(360)
    for idx, h_base in enumerate(cores):
        espiral(x, y, angulo, h_base, idx=idx)
        angulo -= offset


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(360, 0, 0)
    for pos_x, pos_y in ((100, 100), (100, 695), (695, 100), (695, 695)):
        cores = list(range(0, 360, 5))
        shuffle(cores)
        espirais(pos_x, pos_y, cores)
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
