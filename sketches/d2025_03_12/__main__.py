"""2025-03-12
Coleção Rotatio
Coleção de desenhos de rotação
png
Sketch,py5,CreativeCoding
"""

from datetime import date, timedelta
from pathlib import Path

import py5
from PIL import Image

from utils import helpers
from utils.draw import cria_grade_ex

sketch = helpers.info_for_sketch(__file__, __doc__)


def carrega_images() -> list:
    dia = date(2025, 2, 15)
    final = date(2025, 3, 12)
    imagens = []
    while dia < final:
        modulo = f"d{dia:%Y_%m_%d}"
        imagem = f"{dia:%Y-%m-%d}.png"
        path = Path(__file__).parent.parent / modulo / imagem
        img = Image.open(path)
        imagens.append(img)
        dia += timedelta(days=1)
    return imagens


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CORNER)
    py5.blend_mode(py5.BLEND)
    alt = 140
    larg = 140
    grade = cria_grade_ex(py5.width, py5.height, 50, 50, alt, larg, False)
    imagens = carrega_images()
    print(len(imagens))
    for idx, x, idy, y in grade:
        imagem = imagens.pop(0)
        py5.image(imagem, x, y, larg, alt)
        with py5.push_style():
            py5.stroke("#222")
            py5.stroke_weight(3)
            py5.no_fill()
            py5.rect(x, y, larg, alt)

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
