"""2024-10-31
Andy Warhol ❤️ São Paulo
Inspirado em Andy Warhol
png
Sketch,py5,CreativeCoding
"""

from pathlib import Path

import py5
from PIL import Image

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

LOCAL_PATH = Path(__file__).parent

LINHAS = 2
COLUNAS = 2

IMAGENS = [
    "../d2024_10_27/2024-10-27.png",
    "../d2024_10_28/2024-10-28.png",
    "../d2024_10_29/2024-10-29.png",
    "../d2024_10_30/2024-10-30.png",
]


def load_and_resize_image(relative_path: str, largura: int, altura: int) -> Image:
    path = LOCAL_PATH / relative_path
    img = Image.open(path)
    return img.resize((largura, altura))


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.image_mode(py5.CORNER)
    quadro_altura = py5.height // LINHAS
    quadro_largura = py5.width // COLUNAS
    assert (LINHAS * COLUNAS) == len(IMAGENS)
    for idy in range(LINHAS):
        y = idy * quadro_altura
        for idx in range(COLUNAS):
            x = idx * quadro_largura
            img = load_and_resize_image(IMAGENS.pop(), quadro_largura, quadro_altura)
            py5.image(img, x, y)

    helpers.write_legend(sketch=sketch, frame="#000", cor="#FFF")


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
