"""2023-09-12"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import numpy as np
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(py5.color(248, 241, 219))
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(py5.color(0))
    py5.noise_seed(89602)
    py5.no_fill()
    func = py5.sin
    limit = py5.random(60, 120)
    speed = py5.random(1.2, 2.2)
    h1 = 30
    h2 = 240
    x_seed = py5.random_int(180)
    with py5.push_matrix():
        py5.translate(WIDTH // 2, 0)
        xa = np.linspace(-WIDTH, WIDTH, (WIDTH * 3) + 1)
        for i, y_seed in enumerate(range(-200, HEIGHT + 200, 5)):
            h = h1 if i % 2 == 1 else h2
            for x in xa:
                y = func(py5.radians(x // speed))
                y = py5.remap(y, -1, 1, -limit, limit) + y_seed + (py5.noise(x) * 5)
                x += x_seed + (py5.noise(y) * 5)
                s = py5.random_int(60, 80)
                b = 100 - s
                py5.stroke(py5.color(h, s, b))
                weight = py5.random_int(4)
                py5.stroke_weight(weight)
                py5.point(x, y)

    write_legend([py5.color(360, 0, 100)], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
