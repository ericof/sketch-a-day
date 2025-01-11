"""2025-01-11
Impossible day
Um fractal Mandelbrot, que me parecia mágica em 1989
png
Sketch,py5,CreativeCoding,genuary,genuary2025,genuary11
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


MAX_INTERACOES = 100


def mandelbrot(c):
    z = 0
    for i in range(MAX_INTERACOES):
        z = z * z + c
        if abs(z) > 2:
            return i
    return MAX_INTERACOES


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    width, height = py5.width, py5.height
    x0, y0 = -0.6, 0  # Center of the fractal in the complex plane
    zoom = 1600
    for x in range(width):
        for y in range(height):
            real = (x - width / 2) / zoom + x0
            imag = (y - height / 2) / zoom + y0
            c = complex(real, imag)
            m = mandelbrot(c)
            h = ((m / MAX_INTERACOES) * 200) + 160
            b = 100 if m < MAX_INTERACOES else 0
            py5.stroke(h, 100, b)
            py5.point(x, y)
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
