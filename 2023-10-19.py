"""2023-10-19"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from random import shuffle

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

CORES = [
    py5.color(0, 255, 0),
    py5.color(255),
]

BLOCOS = [0, 1, 3, 9, 18, 27, 0, 3, 9]


def popula_area(xi, yi, xf, yf, cores, exp, seed):
    if exp == 0:
        exp = 1
        cores = [
            CORES[1],
        ]
    passo_x = (xf - xi) / exp
    passo_y = (yf - yi) / exp
    for idy in range(0, exp):
        y = yi + (idy * passo_y)
        for idx in range(0, exp):
            x = xi + (idx * passo_x)
            cor = cores[(idx + idy + seed) % len(cores)]
            py5.stroke(cor)
            py5.fill(cor)
            py5.square(x, y, passo_x)


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(py5.color(0))
    x0 = 40
    x1 = WIDTH - x0
    y0 = 40
    y1 = HEIGHT - y0
    passos = 3
    passo_x = (x1 - x0) // passos
    passo_y = (y1 - y0) // passos
    shuffle(BLOCOS)
    i = 0
    for idy in range(0, passos):
        yi = y0 + (idy * passo_y)
        yf = yi + passo_y
        for idx in range(0, passos):
            xi = x0 + (idx * passo_x)
            xf = xi + passo_x
            exp = BLOCOS[i]
            i += 1
            popula_area(xi, yi, xf, yf, CORES, exp, idy)

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
