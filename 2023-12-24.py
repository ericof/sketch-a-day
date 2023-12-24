"""2023-12-24"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

PASSO = WIDTH // 20


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    x0 = WIDTH // 2
    y0 = 40
    y1 = HEIGHT
    for x in range(0, WIDTH, PASSO):
        for i in range(0, 2):
            peso = 4
            h = 150
            x1 = x
            if i:
                peso = 2
                h = 0
                x1 += 6 if x1 <= WIDTH // 2 else -6
            py5.stroke_weight(peso)
            py5.stroke(h, 100, 100)
            py5.line(x0, y0, x1, y1)
    write_legend([py5.color(255, 0, 255)], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
