"""2023-04-18"""
from helpers import HEIGHT
from helpers import save_image
from helpers import tmp_path
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5

IMG_NAME = Path(__file__).name.replace(".py", "")

PATH = tmp_path()

FRAMES = []


def settings():
    py5.size(WIDTH, HEIGHT)


def setup():
    py5.color_mode(py5.HSB)
    py5.no_stroke()
    py5.background("#000000")
    write_legend(["#FFFFFF"], IMG_NAME)
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2)
        for radius in range(100, 350, 30):
            py5.fill(350 - radius, 250, 210, py5.random(45, 120))
            py5.no_stroke()
            w = int(radius / 7)
            for idx in range(0, 360, 3):
                draw_petals(radius, 7, idx, w)
        for radius in range(50, 390, 30):
            py5.fill(300 - radius, 250, 210, 30)
            py5.stroke(300 - radius, 180, 120)
            w = int(radius / 6)
            for idx in range(0, 360, 3):
                draw_petals(radius, 4, idx, w)
    save_image(IMG_NAME)


def draw_petals(radius, angle, idx, w):
    py5.rotate(py5.radians(angle))
    py5.ellipse_mode(py5.CENTER)
    py5.ellipse(0, -radius, w, py5.random(35, 50))


py5.run_sketch()
