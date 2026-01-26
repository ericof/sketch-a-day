"""2026-01-26
Island space
Linhas com uso de espaço negativo.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from pathlib import Path
from PIL import Image
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers
from sketches.utils.helpers.recursos import caminho_arquivo

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)
Z_MASCARA = -45


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
        x += helpers.DIMENSOES.internal[0] // 2
        y += helpers.DIMENSOES.internal[1] // 2
    x = int(x)
    y = int(y)
    try:
        dentro = bool(mascara[x][y])
    except IndexError:
        dentro = False
    return dentro


def pinta_mascara(mascara: np.array, cor: str):
    with py5.push():
        py5.stroke(cor)
        py5.stroke_weight(2)
        for x in range(-400, 401):
            for y in range(-400, 401):
                if dentro_mascara(x, y, mascara, True):
                    py5.point(x, y, Z_MASCARA)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color(0)
    with py5.push():
        py5.background("#222222")
        paleta = gera_paleta("south-africa", True)
        py5.rect_mode(py5.CORNERS)
        py5.stroke_weight(2)
        py5.no_fill()
        caminho = caminho_arquivo("sampa.png")
        mascara = carregar_mascara(caminho)
        passos = 120
        lx = helpers.DIMENSOES.internal[0] // 2
        ly = helpers.DIMENSOES.internal[1] // 2
        x = np.linspace(-lx, lx, endpoint=False, num=helpers.DIMENSOES.internal[0])
        y = np.linspace(-ly, ly + 40, endpoint=True, num=passos)
        multiplicadores = np.logspace(0.9, 1.8, num=passos // 2, endpoint=False)
        multiplicadores = sorted(multiplicadores) + sorted(
            multiplicadores, reverse=True
        )
        pesos = np.linspace(1.2, 2.4, num=passos // 2, endpoint=False)
        pesos = sorted(pesos) + sorted(pesos, reverse=True)
        y = zip(y, multiplicadores, pesos, strict=False)
        with py5.push():
            py5.translate(*helpers.DIMENSOES.centro, -20)
            pinta_mascara(mascara=mascara, cor="#FCF9E6")
            for yb, mult_b, peso in y:
                y0 = None
                x0 = 0
                for idx, x1 in enumerate(x):
                    xd = py5.remap(x1, -lx, lx, -100, 120)
                    mult = mult_b * py5.sin(py5.radians(xd))
                    yd = mult * (
                        abs(
                            py5.sin(py5.radians(x0 + (2 * yb)))
                            * py5.sin(py5.radians(x1 + yb))
                            * py5.sin(py5.radians(x0))
                        )
                    )
                    y1 = yb + yd if (idx % 2) else yb - yd

                    if y0 is None:
                        y0 = y1
                    py5.stroke(paleta[0])
                    py5.stroke_weight(peso)
                    if dentro_mascara(x0, y0, mascara):
                        py5.stroke(paleta[-1])
                        py5.line(x0, y0, Z_MASCARA + 5, x1, y1, Z_MASCARA + 5)
                    else:
                        py5.stroke_weight(1)
                        py5.circle(x1, y1, peso)
                    x0, y0 = x1, y1
                paleta.rotate(1)

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
