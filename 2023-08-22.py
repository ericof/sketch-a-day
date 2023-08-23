"""2023-08-22"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from helpers.circles import Circles
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

FUNDO = (248, 241, 219)


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(py5.color(*FUNDO))
    r = WIDTH
    n = 2100
    fill = (10, 0, 78)
    reverse_fill = FUNDO
    stroke = fill
    circle = Circles(
        cx=WIDTH / 2,
        cy=HEIGHT / 2,
        r=r,
        n=n,
        fill=fill,
        reverse_fill=reverse_fill,
        stroke=stroke,
    )
    circle.populate()
    circle.draw()
    write_legend([py5.color(100)], img_name=IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
