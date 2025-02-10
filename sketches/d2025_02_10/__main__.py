"""2025-02-10
MSX Lives 04
Exercícios a partir de códigos MSX Basic
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

D = 200
G1 = D * 0.75
G2 = D * 0.5
H = 1.5


def calcula_distancia(x, y):
    return py5.sqrt((x**2) + (y**2))


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.stroke_weight(1)
    xc = py5.width // 2
    yc = py5.height // 2
    passo = 0.66
    f = 0
    z = -40
    with py5.push_matrix():
        py5.translate(xc, yc, z)
        while f < py5.TAU:
            for g in range(0, D - 1):
                x0 = D * py5.sin(f + g * 0.1)
                x1 = x0 + G1 * py5.sin(g * 0.1 + f * H)
                y0 = D * py5.cos(f + g * 0.1)
                y1 = y0 + G2 * py5.cos(g * 0.1 + f * H)
                direcao = (
                    -1 if (calcula_distancia(x0, y0) > calcula_distancia(x1, y1)) else 1
                )
                h = int(py5.remap(((x0 + y0) / 2), -150, 150, 120, 360))
                with py5.push_style():
                    peso = 3 if direcao > 0 else 1
                    zb = 5 if direcao > 0 else -60
                    py5.stroke_weight(peso)
                    py5.stroke(py5.color(h, 80, 80))
                    py5.line(x0, y0, 0, x1, y1, zb)
                with py5.push_style():
                    py5.stroke("#000")
                    py5.point(x0, y0)

            f += passo
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
