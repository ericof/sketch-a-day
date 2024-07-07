"""2024-07-07
Memórias 8-bit (1)
Donut formado por Círculos
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


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
    py5.stroke(255)
    raio = 200
    passos = 40
    coordenadas = calcula_coordenadas(py5.width / 2, py5.height // 2, raio, passos)
    for x, y in coordenadas:
        with py5.push_matrix():
            py5.translate(x, y)
            py5.circle(0, 0, raio)
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
