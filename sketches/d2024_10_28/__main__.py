"""2024-10-28
Choque de realidade
A partir de uma grade, colocamos quadrados com pequenas imperfeições
png
Sketch,py5,CreativeCoding
"""

from pathlib import Path
from random import choice, shuffle

import numpy as np
import py5
from PIL import Image

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

PASTA = Path(__file__).parent
MASCARA = PASTA / "sampa.png"

PALETA_SP = [
    "#555",
    "#444",
    "#333",
]

PALETA = [
    "#CCC",
    "#BBB",
    "#AAA",
    "#999",
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


def cria_grade(
    xi: int,
    xf: int,
    yi: int,
    yf: int,
    celula_x: int,
    celula_y: int,
    alternada: bool = True,
):
    """Cria uma grade."""
    pontos = []
    celula_x = int(celula_x)
    celula_y = int(celula_y)
    for idy, y in enumerate(range(yi, yf + 1, celula_y)):
        if (y + celula_y) > yf:
            break
        buffer = int(celula_x / 2) if (alternada and idy % 2) else 0
        for x in range(xi - buffer, xf + 1, celula_x):
            pontos.append((x, y))
    return pontos


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(248, 241, 219)
    py5.rect_mode(py5.CORNER)
    mascara = carregar_mascara(MASCARA)
    shuffle(PALETA)
    margem_x = -200
    margem_y = -200
    largura_base = 5
    altura_base = 5
    grade = cria_grade(
        margem_x,
        py5.width - margem_x,
        margem_y,
        py5.height - margem_y,
        largura_base,
        altura_base,
        True,
    )
    # shuffle(grade)
    for x, y in grade:
        py5.no_stroke()
        mult_l = py5.random(1.1, 1.5)
        mult_a = py5.random(1.2, 1.3)
        largura = largura_base * mult_l
        altura = altura_base * mult_a
        forma = py5.create_shape(py5.RECT, 0, 0, largura, altura)
        rotacao_max = abs(
            py5.remap(y, -200, 1000, 0, 9) * py5.remap(x, -200, 1000, 0, 4)
        )
        if dentro_mascara(x, y, mascara, False):
            cor_interna = choice(PALETA_SP)
        else:
            cor_interna = choice(PALETA)
        py5.fill(cor_interna)
        forma.rotate(py5.radians(py5.random(-rotacao_max, rotacao_max)))
        py5.shape(forma, x, y)
        with py5.push_style():
            py5.stroke_weight(1)
            py5.stroke("#000")
            py5.rect(x, y, largura_base, altura_base)
    with py5.push_matrix():
        py5.translate(0, 0, 10)
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
