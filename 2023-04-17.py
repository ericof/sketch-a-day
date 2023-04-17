"""2023-04-17"""
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
    py5.background("#000000")
    py5.no_stroke()
    write_legend(["#FFFFFF"], IMG_NAME)
    py5.color_mode(py5.HSB)
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2)
        for radius in range(0, 350, 30):
            py5.fill(350 - radius, 250, 210, py5.random(45, 120))
            py5.stroke(radius, 200, 50)
            for idx in range(0, 360, 5):
                draw_petals(radius, 5, idx)
    save_image(IMG_NAME)


def draw_petals(radius, angle, idx):
    py5.rotate(py5.radians(angle))
    py5.ellipse_mode(py5.CENTER)
    py5.ellipse(0, -radius, py5.sin(idx) * py5.random(40) + 20, py5.random(35, 50))


py5.run_sketch()
