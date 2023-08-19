"""2023-08-19"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from random import shuffle

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

FUNDO = py5.color(248, 241, 219)


PONTOS = []


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    desenha()


def desenha():
    py5.background(FUNDO)
    py5.color_mode(py5.HSB, 360, 100, 100)
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2)
        py5.rotate(py5.radians(30))
        y = -HEIGHT
        while y < (HEIGHT + 40):
            y1 = y + py5.random_int(25, 70)
            x = -WIDTH
            while x < (WIDTH + 40):
                x1 = x + py5.random_int(15, 90)
                color = py5.color(py5.random_int(20, 255), 60, 80)
                py5.fill(color)
                py5.rect(x, y, x1 - x, y1 - y)
                x = x1
            y = y1
    write_legend([py5.color(100)], img_name=IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
