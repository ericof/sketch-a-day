"""2024-09-17
Description
Alt
png
Sketch,py5,CreativeCoding
"""

import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def calcula_esfera(num: int, raio: int = 200):
    indices = np.arange(0, num, dtype=float) + 0.5
    phi = np.arccos(1 - 2 * indices / num)
    theta = np.pi * (20 + (5**0.5)) * indices

    x, y, z = np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi)
    pontos = []
    for i in range(0, num):
        pontos.append((x[i] * raio, y[i] * raio, z[i] * raio))
    return pontos


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    raio = 350
    pontos = calcula_esfera(6000, raio)
    py5.stroke_weight(3)
    with py5.push_matrix(), py5.push_style():
        py5.translate(py5.width / 2, py5.height / 2, 0)
        py5.rotate_y(py5.radians(45))
        for x, y, z in pontos:
            h = py5.remap(x, -raio, raio, 0, 360)
            s = py5.remap(x, -raio, raio, 50, 100)
            b = py5.remap(x, -raio, raio, 50, 100)
            cor = py5.color(h, s, b)
            py5.stroke(cor)
            py5.point(x, y, z)
    helpers.write_legend(sketch=sketch, frame="#fff", cor="#000")


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
