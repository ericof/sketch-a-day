"""2023-06-15"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from helpers.poison_disc_sampling import PoissonDiscSampling
from pathlib import Path
from random import shuffle

import numpy as np
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

pds_list = []


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.no_fill()
    py5.frame_rate(1)
    for _ in range(0, 125):
        sep_radius = py5.random(250, 450)
        pds_list.append(
            (
                PoissonDiscSampling(0, 0, WIDTH, HEIGHT, sep_radius, 2, 0, 15),
                py5.color(py5.random(360), py5.random(80, 100), 100, py5.random(2, 5)),
            )
        )


def draw():
    # Set background
    py5.background(0)

    shuffle(pds_list)
    sub_list = pds_list[:8]
    curve_range = py5.random(10, 80)
    num_curves = py5.random_int(6000, 10000)

    # Loop thousands of times, gradually adjusting the curve tightness
    for i in np.linspace(-curve_range, curve_range, num=num_curves):
        py5.curve_tightness(i)
        for idx, (pds, color) in enumerate(sub_list):
            with py5.push_matrix():
                py5.rotate(py5.radians(idx * 30))
                with py5.begin_shape():
                    py5.stroke(color)
                    py5.curve_vertices(pds.point_list)
    write_legend([py5.color(360, 0, 100)], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, extension="png")
        py5.exit_sketch()


py5.run_sketch()
