"""2023-08-26"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from helpers.circles import Circles
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

FUNDO = (0, 0, 0)


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(py5.color(*FUNDO))
    r = WIDTH
    n = 10000
    fill = FUNDO
    reverse_fill = FUNDO
    stroke = (255, 255, 255)
    stroke_weight = 0
    circle = Circles(
        cx=WIDTH / 2,
        cy=HEIGHT / 2,
        r=r,
        n=n,
        rho_min=0.001,
        rho_max=0.05,
        fill=fill,
        reverse_fill=reverse_fill,
        stroke=stroke,
        stroke_weight=stroke_weight,
        circles_r_limit=5,
        guard=400,
        debug=True,
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
