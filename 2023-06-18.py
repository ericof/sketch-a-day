"""2023-06-18"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from helpers.poison_disc_sampling import PoissonDiscSampling
from pathlib import Path
from random import shuffle

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

COLORS = []
points_list = []


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.no_fill()
    py5.frame_rate(1)
    for _ in range(0, 10):
        COLORS.append(
            py5.color(py5.random(360), 100, py5.random(80, 100), py5.random(80, 90))
        )
    total_colors = len(COLORS)
    for _ in range(0, 3):
        sep_radius = 30
        pds = PoissonDiscSampling(0, 0, WIDTH, HEIGHT, sep_radius, 15, 0, 80)
        color_points = [
            (py5.random_int(total_colors - 1), p[0], p[1]) for p in pds.point_list
        ]
        points_list.append(color_points)


def draw():
    # Set background
    py5.background(0)

    shuffle(points_list)
    sub_list = points_list[:3]
    for points in sub_list:
        for color_idx, x, y in points:
            color = COLORS[color_idx]
            py5.stroke(color)
            py5.fill(color)
            py5.circle(x, y, 1)
        color_idx = py5.random_int(len(COLORS) - 1)
        with py5.begin_shape():
            points = [(x, y) for c, x, y in points if c == color_idx]
            color = COLORS[color_idx]
            py5.no_fill()
            py5.stroke(color)
            py5.stroke_weight(3)
            py5.curve_vertices(points)
    write_legend([py5.color(360, 0, 100)], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, extension="png")
        py5.exit_sketch()


py5.run_sketch()
