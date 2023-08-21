"""2023-08-21"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

FUNDO = py5.color(248, 241, 219)


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    desenha()


def desenha():
    py5.background(FUNDO)
    py5.color_mode(py5.HSB, 360, 100, 100)
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2)
        for opacidade in range(100, 20, -5):
            py5.rotate(py5.radians(py5.random_int(0, 180)))
            for y in range(-HEIGHT, HEIGHT, 60):
                for x in range(-WIDTH, WIDTH, 80):
                    color = py5.color(py5.random_int(20, 255), 60, 80, opacidade)
                    height = py5.random_int(30, 80)
                    width = py5.random_int(30, 80)
                    buffer_x = py5.random_int(-10, 10)
                    buffer_y = py5.random_int(-10, 10)
                    s = py5.create_shape(py5.RECT, 0, 0, width, height)
                    s.set_stroke(False)
                    s.set_fill(color)
                    s.rotate(py5.radians(py5.random_int(-30, 30)))
                    py5.shape(s, x + buffer_x, y + buffer_y)
    write_legend([py5.color(100)], img_name=IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
