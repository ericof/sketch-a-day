"""2023-11-29"""
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
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(py5.color(0))
    py5.noise_seed(1200)
    py5.no_fill()
    x_seed = py5.random_int(50)
    altura = HEIGHT // 2
    largura = WIDTH // 2
    with py5.push_matrix():
        py5.translate(largura, altura, 0)
        xa = np.linspace(-largura - 50, largura + 50, WIDTH + 1)
        for i, y_seed in enumerate(range(-altura, +altura, 1)):
            limit = py5.random(30, 40)
            speed = py5.random(0.2, 4.2)
            func = py5.sin if i % 3 == 1 else py5.cos
            for x in xa:
                noise = py5.random_int(0, 60)
                y = func(py5.radians(x // speed))
                y = py5.remap(y, -1, 1, -limit, limit) + y_seed + (py5.noise(x) * noise)
                x += x_seed + (py5.noise(y) * noise)
                h = py5.random_int(0, 360)
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
