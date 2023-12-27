"""2023-12-28"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

PASSO = 15
LIMITE = 500


def setup():
    global PLANETAS
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    with py5.push_matrix():
        py5.translate(WIDTH // 2, HEIGHT // 2, 0)
        py5.rotate_z(py5.radians(45))
        quadrantes = [
            ((0, LIMITE + 1, PASSO), (LIMITE, -1, -PASSO)),
            ((0, -LIMITE - 1, -PASSO), (LIMITE, -1, -PASSO)),
            ((0, -LIMITE - 1, -PASSO), (-LIMITE, 1, PASSO)),
            ((0, LIMITE + 1, PASSO), (-LIMITE, 1, PASSO)),
        ]
        for qx, qy in quadrantes:
            x0_ = [x0 for x0 in range(*qx)]
            y1_ = [y1 for y1 in range(*qy)]
            pontos = list(zip(x0_, y1_))
            total = len(pontos)
            for idx, (x0, y1) in enumerate(pontos):
                x1 = 0
                y0 = 0
                py5.stroke_weight((total - idx) // 10 + 1)
                py5.stroke(160 + (idx * 3), 100, 100)
                py5.line(x0, y0, x1, y1)
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
