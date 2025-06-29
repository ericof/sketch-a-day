"""2025-06-29
Mandelbrot 01
Inspirado por https://msxpen.com/codes/-OTlwobBiV0PyIo6lw1W
png
Sketch,py5,CreativeCoding,fractal,mandelbrot
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def calcula_fractal(h_base=0, h_passo=1.0, cx=-0.5, cy=0.0, escala=1.5):
    pontos = []
    h_limite = h_base + 80

    # Define os limites do plano complexo com base no centro e no zoom
    x_min = cx - escala
    x_max = cx + escala
    y_min = cy - escala * (py5.height / py5.width)
    y_max = cy + escala * (py5.height / py5.width)
    for y in range(py5.height):
        b = py5.remap(y, 0, py5.height, y_min, y_max)
        for x in range(py5.width):
            a = py5.remap(x, 0, py5.width, x_min, x_max)
            zr = 0.0
            zi = 0.0
            h = h_base

            while h < h_limite and (zr * zr + zi * zi) < 8.0:
                t = zr * zr - zi * zi + a
                zi = 2 * zr * zi + b
                zr = t
                h += h_passo

            if h < h_limite:
                mod = zr * zr + zi * zi
                log_zn = py5.log(mod) / 2
                nu = py5.log(log_zn / py5.log(2)) / py5.log(2)
                smooth_h = h + 1 - nu
                escapou = True
            else:
                smooth_h = h
                escapou = False

            pontos.append((x, y, smooth_h, escapou))

    return pontos


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    pontos = calcula_fractal(h_base=80, h_passo=3.2, cx=-0.5, cy=0.0, escala=1.2)
    for x, y, h_base, escapou in pontos:
        if escapou:
            h = (h_base * 5) % 360
            cor = py5.color(h, 100, 100)
        else:
            cor = py5.color(0, 0, 0)
        py5.stroke(cor)
        py5.point(x, y)
    helpers.write_legend(sketch=sketch, frame="#000", cor="#fff")


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
