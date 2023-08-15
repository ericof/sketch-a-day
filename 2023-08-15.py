"""2023-08-14"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from pathlib import Path

import numpy as np
import opensimplex
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

FUNDO = py5.color(248, 241, 219)


noise_x_scale = 0.03
noise_y_scale = 0.05
time_speed = 0.06
noise_generator = opensimplex.seed(6520)


color_palette = [
    (39, 24, 126),
    (117, 139, 253),
    (174, 184, 254),
    (30, 49, 86),
    (164, 2, 222),
    (118, 27, 186),
    (76, 42, 154),
    (172, 135, 223),
    (104, 89, 187),
    (255, 134, 0),
]


def map_value(value, start1, stop1, start2, stop2):
    proportion = (value - start1) / (stop1 - start1)
    return start2 + proportion * (stop2 - start2)


def settings():
    py5.size(WIDTH, HEIGHT, py5.P3D)


def setup():
    py5.background(FUNDO)
    py5.color_mode(py5.RGB, 255)
    py5.no_stroke()
    desenha()


def desenha():
    time = py5.millis() * time_speed
    X = np.arange(0, WIDTH)
    Y = np.arange(0, HEIGHT)
    XN = np.array([x * noise_x_scale for x in X])
    YN = np.array([y * noise_y_scale for y in Y])
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
            py5.no_stroke()
            py5.fill(*c, 80)
            py5.ellipse(x, y, 5, 5)
    img = py5.get_pixels()
    with py5.push_matrix():
        py5.background(py5.color(0))
        py5.translate(WIDTH / 2, HEIGHT / 2, 0)
        py5.ambient_light(255, 102, 255)
        py5.light_specular(204, 204, 204)
        py5.directional_light(200, 200, 200, 0.5, 0, -1)
        sphere = py5.create_shape(py5.SPHERE, 200)
        sphere.set_shininess(10)
        sphere.set_texture(img)
        py5.shape(sphere)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
