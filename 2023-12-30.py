"""2023-12-30"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

DIAMETRO = 350


def setup():
    py5.size(WIDTH, HEIGHT, py5.P2D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(0)
    with py5.push_matrix():
        py5.translate(py5.width / 2, py5.height / 2)
        py5.rotate(py5.radians(180))
        passo = 1
        for i in range(0, 360, passo):
            for y in range(0, DIAMETRO + 1, 3):
                color = py5.color(i, y / 3, 70, 20)
                py5.fill(color)
                py5.stroke(color)
                largura = (y // 7) + 1
                py5.circle(0, y, largura)
            py5.rotate(py5.radians(passo))

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
