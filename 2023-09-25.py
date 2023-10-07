"""2023-09-25"""
from helpers import CelulaV3 as Celula
from helpers import Grade
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

CORES = [
    py5.color(10, 0, 78),
    py5.color(10, 0, 120),
    py5.color(180, 67, 32),
    py5.color(37, 67, 32),
]


def forma_01(x, y, largura, largura_i):
    x_h = x + largura / 2
    y_h = y + largura / 2
    x1 = x + largura
    y1 = y + largura
    # Interno
    buffer_i = (largura - largura_i) / 2
    xi0 = x + buffer_i
    xi1 = xi0 + largura_i
    xih = (largura_i / 2) + xi0
    yi0 = y + buffer_i
    yi1 = yi0 + largura_i
    yih = (largura_i / 2) + yi0
    xbz1 = xi0 + ((largura_i / 2) * 0.45)
    xbz2 = xi1 - ((largura_i / 2) * 0.45)
    ybz1 = yi0 + ((largura_i / 2) * 0.45)
    ybz2 = yi1 - ((largura_i / 2) * 0.45)
    s = py5.create_shape()
    s.set_fill(False)
    s.set_stroke_weight(3)
    with s.begin_shape():
        s.vertex(x, y)
        s.vertex(x1, y)
        s.vertex(x1, y1)
        s.vertex(x, y1)
        s.vertex(x, y)
        with s.begin_contour():
            s.vertex(xi0, yih)
            s.bezier_vertex(xi0, ybz1, xbz1, yi0, xih, yi0)
            s.bezier_vertex(xbz2, yi0, xi1, ybz1, xi1, yih)
            s.bezier_vertex(xi1, ybz2, xbz2, yi1, xih, yi1)
            s.bezier_vertex(xbz1, yi1, xi0, ybz2, xi0, yih)

    return s


def forma_02(x, y, largura, largura_i):
    x1 = x + largura
    y1 = y + largura
    # Interno
    buffer_i = (largura - largura_i) / 2
    xi0 = x + buffer_i
    xi1 = xi0 + largura_i
    xih = (largura_i / 2) + xi0
    yi0 = y + buffer_i
    yi1 = yi0 + largura_i
    yih = (largura_i / 2) + yi0

    s = py5.create_shape()
    s.set_fill(False)
    s.set_stroke_weight(3)
    with s.begin_shape():
        s.vertex(x, y)
        s.vertex(x1, y)
        s.vertex(x1, y1)
        s.vertex(x, y1)
        s.vertex(x, y)
        with s.begin_contour():
            s.vertex(xih, yi0)
            s.vertex(xi1, yih)
            s.vertex(xih, yi1)
            s.vertex(xi0, yih)
            s.vertex(xih, yi0)

    return s


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(py5.color(248, 241, 219))
    write_legend([py5.color(0)], IMG_NAME)
    linhas = 8
    colunas = 8
    margem = 50
    largura = (py5.width - (2 * margem)) / colunas
    grade = Grade(0, 0, WIDTH, HEIGHT, colunas, linhas, margem, margem)
    formas = [
        forma_01(0, 0, largura, largura * 0.8),
        forma_02(0, 0, largura, largura * 0.8),
    ]
    for slot in grade:
        x, y = slot.x, slot.y
        slot.celulas.append(Celula(x, y, largura, formas, CORES))
        x, y = x - 1, y - 1
        slot.celulas.append(Celula(x, y, largura, formas, CORES))

    grade.desenha()


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()