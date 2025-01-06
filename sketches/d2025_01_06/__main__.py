"""2025-01-06
Landscape w/ primitive shapes
A partir de uma foto, criamos uma imagem a partir de elipses
png
Sketch,py5,CreativeCoding,genuary,genuary2025,genuary6
"""

from pathlib import Path

import numpy as np
import py5

from utils import helpers
from utils.draw import rgb_to_hsb

sketch = helpers.info_for_sketch(__file__, __doc__)


def desenha_fundo():
    # Desenha fundo
    for i in range(280, 0, 1 - 10):
        py5.fill(i, i, i)
        tam = 800 + i
        py5.rect(py5.width // 2, py5.height // 2, tam, tam)


def pixelar(img_array: np.array, tam_pixel: int = 24, func=np.median, forma=py5.rect):
    py5.color_mode(py5.HSB, 360, 100, 100)
    # py5.no_stroke()
    for x in range(0, helpers.LARGURA, tam_pixel):
        for y in range(0, helpers.ALTURA, tam_pixel):
            bloco = img_array[y : y + tam_pixel, x : x + tam_pixel]
            cor = func(bloco, axis=(0, 1))
            h, s, b = rgb_to_hsb(cor[0], cor[1], cor[2])
            py5.fill(h, s, b)
            py5.stroke(h, s, b + 10)
            forma(x, y, tam_pixel - 2, tam_pixel - 2)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(200, 200, 200)
    py5.ellipse_mode(py5.CENTER)
    py5.rect_mode(py5.CENTER)
    path = Path(__file__).parent / "landscape.jpg"
    img_array = helpers.image_as_array(path)
    with py5.push_matrix():
        py5.translate(0, 0, -60)
        desenha_fundo()
        pixelar(img_array, 8, np.average, py5.ellipse)
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
