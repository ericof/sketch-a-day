"""2024-04-28
Espiral V
Criação de seis espirais formadas por círculos
png
Sketch,py5,CreativeCoding,grid
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def espirais(x: float, y: float, cores: list[int] | None = None):
    total_cores = len(cores)
    offset = 360 / total_cores
    angulo = 0
    for idx, h_base in enumerate(cores):
        espiral(x, y, angulo, h_base, idx)
        angulo -= offset


def espiral(x0: float, y0: float, offset: float, h_base: float = 40, idx: int = 0):
    reverso = 1 if (idx % 2 == 1) else -1
    pontos = 1200
    raio_max = 900
    for i in range(pontos):
        angulo = py5.radians((i * 5 + offset) * reverso)
        r = i * raio_max / pontos
        x_diff = r * (1.2 * py5.cos(angulo)) * reverso
        x = x0 + x_diff
        y_diff = r * (0.9 * py5.sin(angulo)) * reverso
        y = y0 - y_diff
        multiplicador = r / 200
        h = h_base + (2 * multiplicador)
        s = 50 + (1 * multiplicador)
        b = 80 + (0.8 * multiplicador)
        py5.stroke(h, s, b)
        py5.fill(h, s, b)
        if i == 0:
            py5.circle(x, y, 3)
        else:
            py5.circle(x, y, 7 * multiplicador)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(360, 0, 0)
    cores = [0, 60, 120, 180, 240, 300]
    espirais(400, 400, cores)
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
