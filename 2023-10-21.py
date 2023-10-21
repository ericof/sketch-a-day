"""2023-10-19"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from random import shuffle

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

COR_SELO = py5.color(188, 0, 45)

CORES = [
    py5.color(223, 227, 16),
]


def popula_area(xi, yi, xf, yf, cores, borda, exp):
    passo_x = (xf - xi) / exp
    passo_y = (yf - yi) / exp
    for idy in range(0, exp):
        y0 = yi + (idy * passo_y)
        y = y0 + (borda // 2)
        tamanho = (y + passo_y - (borda // 2)) - y
        for idx in range(0, exp):
            x0 = xi + (idx * passo_x)
            x = x0 + (borda // 2)
            cor = cores[(idx + idy) % len(cores)]
            py5.stroke(cor)
            py5.fill(cor)
            py5.square(x, y, tamanho)
    tamanho = xf - xi
    x = tamanho // 2 + xi
    y = tamanho // 2 + yi
    tamanho = tamanho // 3
    py5.stroke(COR_SELO)
    py5.fill(COR_SELO)
    py5.circle(x, y, tamanho)


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(py5.color(0))
    x0 = 40
    x1 = WIDTH - x0
    y0 = 40
    y1 = HEIGHT - y0
    passos = 3
    exp = 7
    borda = 20
    borda_interna = 6
    passo_x = (x1 - x0) // passos
    passo_y = (y1 - y0) // passos
    for idy in range(0, passos):
        yi = y0 + (idy * passo_y) + (borda // 2)
        yf = yi + passo_y - (borda // 2)
        for idx in range(0, passos):
            xi = x0 + (idx * passo_x) + (borda // 2)
            xf = xi + passo_x - (borda // 2)
            popula_area(xi, yi, xf, yf, CORES, borda_interna, exp)

    write_legend([py5.color(255)], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
