"""2023-05-24"""
from helpers import HEIGHT
from helpers import save_frame
from helpers import save_gif
from helpers import tmp_path
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import numpy as np
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")
PATH = tmp_path()

FRAMES = []

PONTOS = []


def gera_cor():
    return py5.color(
        py5.random_int(0, 100),
        py5.random_int(40, 100),
        py5.random_int(90, 100),
    )


def gera_pontos(points: int):
    rng = np.random.default_rng()
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    z1 = 800 / 2
    x0 = -x1
    y0 = -y1
    z0 = -z1
    raw = rng.uniform([x0, y0, z0], [x1, y1, z1], size=(points, 3))
    return [[x, y, z, py5.random_int(1, 6), gera_cor()] for x, y, z in raw]


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.color_mode(py5.HSB, 100, 100, 100)
    p = 35000
    py5.frame_rate(15)
    PONTOS.extend(gera_pontos(p))


def draw():
    frame = py5.frame_count
    passo = frame % 360
    py5.background(0)
    write_legend([py5.color(100)], img_name=IMG_NAME)
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2, -700)
        py5.rotate_x(py5.radians(passo))
        py5.rotate_y(py5.radians(passo))
        for x, y, z, weight, color in PONTOS:
            py5.stroke_weight(weight)
            py5.stroke(color)
            py5.point(x, y, z)
    if frame % 4 == 1:
        FRAMES.append(save_frame(PATH, IMG_NAME, frame))
    if len(FRAMES) > 45:
        print("Too many frames")
        py5.no_loop()
    py5.window_title(f"FR: {py5.get_frame_rate():.1f} | Frame Count: {frame} {passo}")


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_gif(IMG_NAME, FRAMES, duration=100)
        py5.exit_sketch()


py5.run_sketch()
