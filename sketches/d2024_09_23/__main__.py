"""2024-09-23
Selfie 03
Esferas + selfie, what could go wrong
png
Sketch,py5,CreativeCoding
"""

import cv2
import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

MARGEM = 100
LINHAS = 3
COLUNAS = 3
ALTURA = (helpers.ALTURA - 2 * MARGEM) // LINHAS
LARGURA = (helpers.LARGURA - 2 * MARGEM) // COLUNAS
IMAGE = None

GRADE = []

movie = cv2.VideoCapture(0)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.sphere_detail(50)
    x0 = MARGEM + (LARGURA // 2)
    xf = (py5.width - MARGEM) + (LARGURA // 2)
    xa = np.linspace(x0, xf, num=COLUNAS, endpoint=False)
    y0 = MARGEM + (ALTURA // 2)
    yf = (py5.height - MARGEM) + (ALTURA // 2)
    ya = np.linspace(y0, yf, num=LINHAS, endpoint=False)
    for x in xa:
        for y in ya:
            cor = py5.color(160, 0, 100)
            forma = py5.create_shape(py5.SPHERE, LARGURA // 2.5)
            forma.set_fill(cor)
            forma.set_stroke(False)
            forma.set_shininess(1.0)
            GRADE.append((forma, x, y))


def draw():
    global IMAGE
    count = py5.frame_count
    py5.rect_mode(py5.CENTER)
    py5.background(0)
    py5.lights()
    py5.directional_light(10, 80, 100, py5.sin(count) * 200, py5.cos(count) * 200, -400)
    for idx, (forma, x, y) in enumerate(GRADE):
        with py5.push_matrix():
            py5.translate(x, y, 0)
            _, frame = movie.read()
            angulo_x = idx * 2 * count
            angulo_y = idx * 2 * count
            angulo_z = idx * 2 * count
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            IMAGE = py5.create_image_from_numpy(frame, "RGBA", dst=IMAGE)
            forma.set_texture(IMAGE)
            forma.rotate_x(py5.radians(angulo_x))
            forma.rotate_y(py5.radians(angulo_y))
            forma.rotate_x(py5.radians(angulo_z))
            py5.shape(forma)
            py5.translate(0, 0, -200)
            w = LARGURA
            h = ALTURA
            fundo = py5.create_shape(py5.RECT, 0, 0, w, h)
            h = abs((2 * py5.sin(idx * 40 * count)) * 180)
            fundo.set_fill(py5.color(h, 80, 80))
            py5.shape(fundo)

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
