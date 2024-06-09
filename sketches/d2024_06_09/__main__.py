"""2024-06-09
Espiral Redux 2
Criação de espirais formadas por círculos
png
Sketch,py5,CreativeCoding,grid
"""

from random import shuffle

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def espirais(x: float, y: float, cores: list[int] | None = None):
    total_cores = len(cores)
    offset = (360 / total_cores) + py5.random_int(5)
    angulo = py5.random_int(20)
    for h_base in cores:
        espiral(x, y, angulo, h_base)
        angulo -= offset


def espiral(x0: float, y0: float, offset: float, h_base: float = 40):
    pontos = 800
    raio_max = 900
    for i in range(pontos):
        angulo = py5.radians(i * 5 - offset)
        r = i * raio_max / pontos
        x = x0 + r * py5.cos(angulo)
        y = y0 + r * py5.sin(angulo)
        multiplicador = py5.sin(py5.radians(r)) * (r / 200)
        h = h_base + (2 * multiplicador)
        s = 50 + (1 * multiplicador * py5.sin(angulo))
        b = 80 + (0.8 * multiplicador * py5.cos(angulo))
        py5.stroke(h, s, b)
        py5.fill(h, s, b)
        if i == 0:
            py5.circle(x, y, 2)
        else:
            py5.circle(x, y, 5 * multiplicador)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(360, 0, 100)
    cores = list(range(0, 360, 15))
    shuffle(cores)
    espirais(200, 200, cores)
    espirais(600, 600, cores)
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
