"""2024-09-21
Selfie 01
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


movie = cv2.VideoCapture(0)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5_img = None
    largura_quadro = py5.width - 2 * MARGEM
    altura_quadro = py5.height - 2 * MARGEM
    largura = largura_quadro // COLUNAS
    altura = altura_quadro // LINHAS
    xa = np.linspace(MARGEM, py5.width - MARGEM, num=COLUNAS, endpoint=False)
    ya = np.linspace(MARGEM, py5.height - MARGEM, num=LINHAS, endpoint=False)
    py5.sphere_detail(50)
    py5.lights()
    py5.directional_light(120, 80, 100, 0.5, 0, -1)
    idx = 0
    for x0 in xa:
        xm = x0 + largura // 2
        idx += 1
        for y0 in ya:
            ym = y0 + altura // 2
            idx += 1
            cor = py5.color(30, 40, 50)
            with py5.push_matrix():
                py5.translate(xm, ym, 0)
                py5.fill(cor)
                py5.no_stroke()
                py5.shininess(3.0)
                _, frame = movie.read()
                angulo_x = idx * 5
                angulo_y = idx * 15
                angulo_z = idx * 5
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                py5_img = py5.create_image_from_numpy(frame, "RGBA", dst=py5_img)
                forma = py5.create_shape(py5.SPHERE, largura // 2.5)
                forma.set_texture(py5_img)
                forma.rotate_x(py5.radians(angulo_x))
                forma.rotate_y(py5.radians(angulo_y))
                forma.rotate_x(py5.radians(angulo_z))
                py5.shape(forma)

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
