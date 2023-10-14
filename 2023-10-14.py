"""2023-10-14"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(py5.color(255))
    with py5.push_matrix():
        py5.translate(WIDTH // 2, HEIGHT // 2)
        cor = py5.color(188, 0, 45)
        py5.fill(cor)
        py5.stroke(cor)
        py5.circle(0, 0, 300)

    write_legend([py5.color(0)], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
