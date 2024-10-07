"""2024-10-07
Ilha digital 04
Estudo sobre formação e conexões de uma cidade desconectado
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from pathlib import Path

import numpy as np
import py5
from PIL import Image

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

PASTA = Path(__file__).parent
MASCARA = PASTA / "sampa.png"

PALETA = deque(
    [
        "#7ec0e0",
        "#1c8eaf",
        "#032035",
        "#fdaa08",
        "#f87109",
    ]
)


def carregar_mascara(imagem: Path):
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


def pinta_mascara(mascara: np.array, cor: str):
    with py5.push_style():
        py5.stroke(cor)
        py5.stroke_weight(2)
        for x in range(0, py5.width):
            for y in range(0, py5.height):
                if dentro_mascara(x, y, mascara, False):
                    py5.point(x, y)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background("#888888")
    py5.rect_mode(py5.CORNERS)
    py5.stroke_weight(2)
    py5.no_fill()
    mascara = carregar_mascara(MASCARA)
    passos = 80
    lx = py5.width // 2
    ly = py5.height // 2
    x = np.linspace(-lx, lx, endpoint=False, num=py5.width)
    y = np.linspace(-ly, ly + 40, endpoint=True, num=passos)
    multiplicadores = np.logspace(0.9, 1.8, num=passos // 2, endpoint=False)
    multiplicadores = sorted(multiplicadores) + sorted(multiplicadores, reverse=True)
    pesos = np.linspace(1.0, 2.4, num=passos // 2, endpoint=False)
    pesos = sorted(pesos) + sorted(pesos, reverse=True)
    y = zip(y, multiplicadores, pesos)
    pinta_mascara(mascara=mascara, cor="#FCF9E6")
    with py5.push_matrix():
        py5.translate(lx, ly)
        for yb, mult_b, peso in y:
            y0 = None
            x0 = 0
            inicio_mascara = None
            for idx, x1 in enumerate(x):
                xd = py5.remap(x1, -lx, lx, -80, 80)
                mult = mult_b * py5.sin(py5.radians(xd))
                yd = mult * (
                    abs(
                        py5.sin(py5.radians(x0 + (3 * yb)))
                        * py5.cos(py5.radians(x1 + yb))
                        * py5.sin(py5.radians(x0))
                    )
                )
                y1 = yb + yd if (idx % 2) else yb - yd

                if y0 is None:
                    y0 = y1
                if dentro_mascara(x0, y0, mascara):
                    py5.stroke(PALETA[0])
                    py5.stroke_weight(peso)
                    py5.circle(x0, y0, peso)
                else:
                    if not inicio_mascara:
                        inicio_mascara = x1
                    py5.stroke_weight(peso)
                    py5.stroke("#FFFFFF")
                    py5.point(x1, y1)
                x0, y0 = x1, y1
            PALETA.rotate(1)
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
