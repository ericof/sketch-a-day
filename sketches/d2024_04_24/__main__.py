"""2024-04-24
Espiral I
Criação de uma espiral de círculos
png
Sketch,py5,CreativeCoding,grid
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def espirais(x: float, y: float, numero: int, offset: float = 0.0):
    if not offset:
        offset = 360 / numero
    angulo = 0
    for _ in range(numero):
        espiral(x, y, angulo)
        angulo += offset


def espiral(x0: float, y0: float, offset: float):
    pontos = 500
    raio_max = 900
    for i in range(pontos):
        angle = py5.radians(i * 5 + offset)
        r = i * raio_max / pontos
        x = x0 + r * py5.cos(angle)
        y = y0 + r * py5.sin(angle)
        multiplicador = r / 120
        h = 40 + (2 * multiplicador)
        s = 100
        b = 80 + (0.8 * multiplicador)
        py5.stroke(h, s, b)
        py5.fill(h, s, b)
        if i == 0:
            py5.circle(x, y, 5)
        else:
            py5.circle(x, y, 5 * multiplicador)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(230, 100, 50)
    espirais(400, 400, 3, 120)
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
