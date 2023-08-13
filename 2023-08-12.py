"""2023-08-12"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from pathlib import Path

import numpy as np
import opensimplex
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

FUNDO = py5.color(248, 241, 219)


noise_scale = 0.005
time_speed = 0.015
noise_generator = opensimplex.seed(6954)


color_palette = [
    (30, 86, 49),
    (164, 222, 2),
    (118, 186, 27),
    (76, 154, 42),
    (172, 223, 135),
    (104, 187, 89),
]


def map_value(value, start1, stop1, start2, stop2):
    proportion = (value - start1) / (stop1 - start1)
    return start2 + proportion * (stop2 - start2)


def settings():
    py5.size(WIDTH, HEIGHT, py5.P2D)


def setup():
    py5.background(FUNDO)
    py5.color_mode(py5.RGB, 255)
    py5.no_stroke()
    desenha()


def desenha():
    time = py5.millis() * time_speed
    X = np.arange(0, WIDTH)
    Y = np.arange(0, HEIGHT)
    XN = np.array([x * noise_scale for x in X])
    YN = np.array([y * noise_scale for y in Y])
    noise_val = opensimplex.noise3array(
        XN,
        YN,
        np.array(
            [
                time,
            ]
        ),
    )
    for idx, x in enumerate(X):
        for idy, y in enumerate(Y):
            if idx % 2 or idy % 2:
                continue
            noise = noise_val[0][idy][idx]
            color_idx = int(map_value(noise, -1, 1, 0, len(color_palette)))
            c = color_palette[color_idx]
            py5.fill(*c, 80)
            py5.ellipse(x, y, 12, 12)
            py5.fill(*c, 80)
            py5.ellipse(y, x, 6, 6)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
