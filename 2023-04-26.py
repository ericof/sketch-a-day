"""2023-04-26"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

FRAMES = []


def settings():
    py5.size(WIDTH, HEIGHT)


def setup():
    background()
    py5.color_mode(py5.RGB)
    py5.frame_rate(10)
    logo()
    write_legend(["#FFFFFF"], IMG_NAME)
    save_image(IMG_NAME, "png")


def background():
    py5.background(0)


def logo():
    plone_color = py5.color("#0083BE")
    diametro = 600
    diametro_interno = 130
    with py5.push_matrix():
        py5.translate(py5.width / 2, py5.height / 2)
        py5.stroke_weight(1)
        py5.stroke(plone_color)
        py5.no_fill()
        passo = 8
        # Borda
        for i in range(477, diametro + 1, passo):
            py5.circle(0, 0, i)
        # Circulo 1
        for i in range(0, diametro_interno + 1, passo):
            py5.circle(93, 0, i)
        x = -40
        y = 131
        # Circulo 2
        for i in range(0, diametro_interno + 1, passo):
            py5.circle(x, -y, i)
        # Circulo 3
        for i in range(0, diametro_interno + 1, passo):
            py5.circle(x, y, i)


py5.run_sketch()
