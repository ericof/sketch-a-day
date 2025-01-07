"""2025-01-07
Landscape with spheres
A partir de uma foto, criamos uma imagem a partir de esferas
png
Sketch,py5,CreativeCoding,genuary,genuary2025
"""

from pathlib import Path

import numpy as np
import py5

from utils import helpers
from utils.draw import rgb_to_hsb

sketch = helpers.info_for_sketch(__file__, __doc__)

TAM_PIXEL = 10


def desenha_fundo():
    # Desenha fundo
    for i in range(280, 0, 1 - 10):
        py5.fill(i, i, i)
        tam = 800 + i
        py5.rect(py5.width // 2, py5.height // 2, tam, tam)


def pixelar(img_array: np.array, tam_pixel: int = 24, func=np.median):
    pontos = []
    # py5.no_stroke()
    for idx, x in enumerate(range(0, helpers.LARGURA, tam_pixel)):
        for idy, y in enumerate(range(0, helpers.ALTURA, tam_pixel)):
            bloco = img_array[y : y + tam_pixel, x : x + tam_pixel]
            cor = func(bloco, axis=(0, 1))
            h, s, b = rgb_to_hsb(cor[0], cor[1], cor[2])
            pontos.append((idx, idy, x, y, (h, s, b)))
    return pontos


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    path = Path(__file__).parent / "landscape.jpg"
    img_array = helpers.image_as_array(path)
    pontos = pixelar(img_array, TAM_PIXEL, np.average)
    py5.no_stroke()
    with py5.push_matrix():
        py5.translate(py5.width // 2, py5.height / 6, 0)
        py5.rotate_x(45)
        py5.lights()
        for idx, idy, xb, yb, cor in pontos:
            x = idx * TAM_PIXEL * 2 - 800
            y = idy * TAM_PIXEL * 2 - 800
            z = idy * -10 + 80
            with py5.push_matrix():
                py5.translate(x, y, z)
                py5.fill(*cor)
                py5.sphere(8)

    helpers.write_legend(sketch=sketch, frame="#666", cor="#FFF")


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
