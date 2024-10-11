"""2024-10-11
Ilha digital 08
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
        "#032035",
        "#120D2D",
        "#1C8EAF",
        "#425AC6",
        "#7EC0E0",
        "#CAC9D1",
        "#D0341E",
        "#F7D744",
        "#F87109",
        "#FDAA08",
    ]
)


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
    py5.background("#222222")
    py5.stroke_weight(1)
    py5.no_fill()
    mascara = carregar_mascara(MASCARA)
    passos = 80
    lx = py5.width // 2
    ly = py5.height // 2
    x = np.linspace(-lx, lx, endpoint=False, num=py5.width)
    y = np.linspace(-ly, ly + 40, endpoint=True, num=passos)
    multiplicadores = np.logspace(0.9, 1.5, num=passos // 2, endpoint=False)
    multiplicadores = sorted(multiplicadores) + sorted(multiplicadores, reverse=True)
    pesos = np.linspace(1.2, 2.4, num=passos // 2, endpoint=False)
    pesos = sorted(pesos) + sorted(pesos, reverse=True)
    y = zip(y, multiplicadores, pesos)
    pinta_mascara(mascara=mascara, cor="#FCF9E6")
    with py5.push_matrix():
        py5.translate(lx, ly)
        for yb, mult_b, peso in y:
            y0 = None
            x0 = 0
            for idx, x1 in enumerate(x):
                xd = py5.remap(x1, -lx, lx, -100, 120)
                mult = mult_b * 2 * py5.cos(py5.radians(xd))
                yd = mult * (
                    abs(
                        py5.sin(py5.radians(x0 + (2 * yb)))
                        * py5.cos(py5.radians(x1 + yb))
                        * py5.sin(py5.radians(x0))
                    )
                )
                y1 = yb + yd if (idx % 2) else yb - yd

                if y0 is None:
                    y0 = y1
                py5.stroke(PALETA[0])
                py5.stroke_weight(peso)
                if dentro_mascara(x0, y0, mascara):
                    py5.stroke(PALETA[-1])
                    py5.line(x0, y0, x1, y1)
                else:
                    py5.stroke_weight(1)
                    py5.circle(x1, y1, peso)
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
