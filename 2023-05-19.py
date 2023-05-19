"""2023-05-19"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

FUNDO = py5.color(0)

CENTRO_X = WIDTH // 2
CENTRO_Y = HEIGHT // 2

MARGEM_X = WIDTH * 0.1
MARGEM_Y = WIDTH * 0.1

rotate_x = 0


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)


def draw():
    global rotate_x
    limite_x = CENTRO_X - MARGEM_X
    limite_y = CENTRO_Y - MARGEM_Y
    py5.background(FUNDO)
    py5.no_fill()
    with py5.push_matrix():
        py5.translate(CENTRO_X, CENTRO_Y, -50)
        py5.rotate_x(py5.radians(rotate_x))
        for passo in range(50, 650, 15):
            peso_base = passo // 150
            py5.stroke(255, 220, 115)
            py5.stroke_cap(py5.ROUND)
            py5.stroke_weight(peso_base + py5.random(0.1, 1.1))
            py5.triangle(
                -limite_x,
                -limite_y,
                -limite_x,
                -limite_y + passo,
                -limite_x + (passo / 1.45),
                -limite_y,
            )
            py5.stroke(235, 200, 95)
            py5.stroke_cap(py5.SQUARE)
            py5.stroke_weight(peso_base + py5.random(0.1, 1.1))
            py5.triangle(
                limite_x,
                limite_y,
                limite_x,
                limite_y - passo,
                limite_x - (passo / 1.5),
                limite_y,
            )

    write_legend([py5.color(255)], img_name=IMG_NAME)


def key_pressed():
    global rotate_x
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, "png")
        py5.exit_sketch()
    elif py5.key_code == 38:
        rotate_x += 1
        print(rotate_x)
    elif py5.key_code == 40:
        print(rotate_x)
        rotate_x -= 1


py5.run_sketch()
