"""2024-07-14
Memórias 8-bit (6)
Donut disforme formado por elipses
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
        y = y0 + (py5.sin(py5.radians(angulo)) * r * 1.15)
        coordenadas.append((x, y))
    return coordenadas


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(40, 40, 40)
    py5.no_fill()
    raio = 200
    passos = 100
    coordenadas = calcula_coordenadas(py5.width / 2, py5.height // 2, raio, passos)
    for idx, (x, y) in enumerate(coordenadas):
        with py5.push_matrix():
            py5.translate(x, y)
            if idx % 2 == 1:
                py5.stroke(51, 255, 51)
            else:
                py5.stroke(255, 176, 0)
            mult = py5.sin(py5.radians(idx) * 1.2) + py5.cos(py5.radians(idx) * 1.5)
            py5.ellipse(0, 0, raio * mult, raio)

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
