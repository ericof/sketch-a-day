"""2025-01-30
Abstract map (Wunderbar)
Du bist so wunderbar, Berlin!
png
Sketch,py5,CreativeCoding,genuary,genuary30
"""

from pathlib import Path
from random import choice

import numpy as np
import py5
from PIL import Image

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)

PASTA = Path(__file__).parent
MASCARA = PASTA / "berlin.png"

PALETA_BLN = [
    "#E50000",
    "#FF8D00",
    "#FFEE00",
    "#028121",
    "#004CFF",
    "#760088",
]

PALETA = [
    "#999",
    "#AAA",
    "#BBB",
    "#CCC",
]


def carregar_mascara(imagem: Path, escala: float = 1):
    """Carrega imagem e retorna a máscara."""

    img = Image.open(imagem)
    img_ = np.array(img.getdata()).reshape(img.height, img.width, 4)
    mask = []
    for y in img_:
        for x in y:
            mask.append(x[3])
    img_ = np.array(mask).reshape(img.height, img.width).transpose()
    return img_


def dentro_mascara(x: float, y: float, mascara: np.array, centrado: bool = True):
    if centrado:
        x += py5.width // 2
        y += py5.height // 2
    x = int(x)
    y = int(y)
    try:
        dentro = bool(mascara[x][y])
    except IndexError:
        dentro = False
    return dentro


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(248, 241, 219)
    py5.blend_mode(py5.BLEND)
    py5.ellipse_mode(py5.CORNER)
    mascara = carregar_mascara(MASCARA)
    margem_x = -200
    margem_y = -200
    largura_base = 4
    altura_base = 4
    grade = cria_grade(
        py5.width - margem_x,
        py5.height - margem_y,
        margem_x,
        margem_y,
        largura_base,
        altura_base,
        True,
    )
    with py5.push_matrix():
        py5.translate(0, 0, -30)
        for x, y in grade:
            py5.no_stroke()
            mult_l = py5.random(1.1, 1.5)
            mult_a = py5.random(1.1, 1.5)
            largura = largura_base * mult_l
            altura = altura_base * mult_a
            forma = py5.create_shape(py5.ELLIPSE, 0, 0, largura, altura)
            cor_interna = (
                choice(PALETA_BLN)
                if dentro_mascara(x, y, mascara, False)
                else choice(PALETA)
            )
            py5.fill(cor_interna)
            py5.shape(forma, x, y)
            with py5.push_style():
                py5.stroke_weight(1)
                py5.stroke("#000")
                py5.ellipse(x, y, largura_base, altura_base)
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
