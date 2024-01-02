"""2024-01-02
Genuary 02 - Sem Paleta de Cores.
Duas matrizes formadas por círculos e quadrados com diversas cores.
png
Sketch,py5,CreativeCoding,genuary,genuary2
"""
import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

MARGEM = 80


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P2D)
    limite_x = helpers.LARGURA // 2
    limite_y = helpers.ALTURA // 2
    py5.background(0)
    py5.rect_mode(py5.CENTER)
    py5.color_mode(py5.HSB, 360, 100, 100)
    x = np.linspace(-limite_x + MARGEM, limite_x - MARGEM, num=180, endpoint=True)
    y = np.linspace(-limite_y + MARGEM, limite_x - MARGEM, num=50, endpoint=True)
    iteracoes = [(0, 90, py5.circle), (45, 40, py5.square)]
    for angulo, t, func in iteracoes:
        with py5.push_matrix():
            py5.translate(limite_x, limite_y)
            py5.rotate(py5.radians(angulo))
            for idy, y0 in enumerate(y):
                for idx, x0 in enumerate(x):
                    h = idx * 2
                    s = abs(50 - (idy * 2)) + 50
                    b = 80
                    cor = py5.color(h, s, b, t)
                    py5.fill(cor)
                    py5.stroke(cor)
                    func(x0, y0, 20)
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
