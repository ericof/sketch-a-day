"""2023-09-01"""
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
    py5.noise_seed(920)
    py5.frame_rate(5)


def draw():
    frame = py5.frame_count
    py5.stroke(py5.color(360, 0, 100))
    py5.stroke_weight(1)
    py5.no_fill()
    func = py5.sin if frame % 2 == 0 else py5.cos
    limit = py5.random(20, 120)
    speed = py5.random(2, 4)
    h = py5.random_int(0, 360)
    s = py5.random_int(60, 80)
    b = py5.random_int(60, 80)
    x_seed = py5.random_int(120)
    y_seed = py5.random_int(-150, 100)
    with py5.push_matrix():
        py5.translate(WIDTH // 2, HEIGHT // 2, -frame)
        py5.rotate_y(py5.radians(frame))
        xa = np.linspace(-WIDTH, WIDTH, (WIDTH * 2) + 1)
        forma = py5.create_shape()
        with forma.begin_shape():
            forma.stroke(py5.color(h, s, b))
            forma.stroke_weight(2)
            for x in xa:
                y = func(py5.radians(x // speed))
                y = py5.remap(y, -1, 1, -limit, limit) + y_seed
                x += x_seed
                forma.vertex(x, y)
                x += py5.noise(y) * (frame % 20)
                y += py5.noise(x) * (frame % 10)
                py5.stroke(py5.color(h, s + 20, b - 15))
                py5.stroke_weight(4)
                py5.point(x, y)

        py5.shape(forma)

    py5.window_title(f"FR: {py5.get_frame_rate():.1f} | Frame Count: {frame}")
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
