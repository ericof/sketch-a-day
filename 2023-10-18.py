"""2023-10-18"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

CORES = [
    py5.color(10, 20, 62),
    py5.color(160, 132, 30),
    py5.color(113, 22, 24),
    py5.color(255),
    py5.color(162, 72, 21),
]


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(py5.color(0))
    py5.rect_mode(py5.CORNERS)
    py5.stroke_weight(6)
    meio_x = WIDTH // 2
    meio_y = HEIGHT // 2
    with py5.push_matrix():
        y0 = -(meio_y - 100)
        y1 = meio_y - 100
        passo = WIDTH // 6
        passo_y = (y1 - y0) // 5
        py5.translate(meio_x, meio_y)
        py5.rotate_z(py5.radians(85))
        # Colunas 0 - 4
        for idx in range(0, 5):
            x = -(meio_x - (idx * passo))
            py5.stroke(CORES[idx])
            py5.fill(CORES[idx])
            py5.rect(x, y0, x + passo, y1)
        x = x + passo
        for idy in range(0, 5):
            y = y0 + (idy * passo_y)
            py5.stroke(CORES[idy])
            py5.fill(CORES[idy])
            py5.rect(x, y, x + passo, y + passo_y)
    write_legend([py5.color(255)], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
