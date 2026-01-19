"""2026-01-19
Pixelate South Africa 01
Exercício de pixelar a bandeira da África do Sul
ericof.com
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers
from sketches.utils.helpers.images import image_as_array
from sketches.utils.helpers.recursos import caminho_arquivo

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)


def pixelate(img_array: np.ndarray, bloco: int = 10):
    py5.no_stroke()
    total_x = len(img_array[0])
    total_y = len(img_array)
    slots_x = range(0, total_x, bloco)
    slots_y = range(0, total_y, bloco)
    for x in slots_x:
        for y in slots_y:
            block = img_array[y : y + bloco, x : x + bloco]
            avg_color = np.median(block, axis=(0, 1))
            py5.fill(avg_color[0], avg_color[1], avg_color[2], 100)
            py5.rect(x, y, bloco, bloco)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color(0)
    py5.background(cor_fundo)
    # py5.color_mode(py5.HSB, 360, 100, 100)x
    arquivo = caminho_arquivo("flag-za.png")
    img_array = image_as_array(arquivo)
    altura = len(img_array)
    largura = len(img_array[0])
    x = (helpers.DIMENSOES.external[0] - largura) / 2
    y = (helpers.DIMENSOES.external[1] - altura) / 2
    with py5.push():
        py5.translate(x, y, -20)
        pixelate(img_array)

    # Credits and go
    canvas.sketch_frame(
        sketch, cor_fundo, "large_transparent_white", "transparent_white"
    )


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
