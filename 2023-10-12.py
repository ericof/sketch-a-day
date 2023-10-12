"""2023-10-12"""
from helpers import CelulaV4 as Celula
from helpers import Grade
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
    py5.stroke_weight(5)
    x = 0
    for y_step in range(0, int(HEIGHT * 1.5), HEIGHT // 5):
        for x0 in range(0, WIDTH):
            if (x0 // 50) % 2 == 0:
                mult = 90
                py5.stroke(py5.color(255, 0, 0))
                x = x0
                func = py5.cos
            else:
                mult = 95
                py5.stroke(py5.color(0))
                x = x0
                func = py5.sin
            y = (func(py5.radians(x))) * mult + y_step
            py5.point(x, y)
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
