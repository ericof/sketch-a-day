"""2023-05-17"""
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


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    limite_x = CENTRO_X - MARGEM_X
    limite_y = CENTRO_Y - MARGEM_Y
    py5.background(FUNDO)
    py5.no_fill()
    py5.stroke(255, 220, 115)
    x = MARGEM_X // 3
    y = MARGEM_Y // 3
    with py5.push_matrix():
        py5.translate(CENTRO_X, CENTRO_Y, -100)
        for passo in range(50, 300, 30):
            py5.stroke_weight(passo // 50 + py5.random(0.1, 1.1))
            py5.triangle(
                -limite_x,
                -limite_y,
                -limite_x,
                -limite_y + passo,
                -limite_x + (passo / 1.5),
                -limite_y,
            )
            py5.stroke_weight(passo // 50 + py5.random(0.1, 1.1))
            py5.rect(-passo / 3.33, -limite_y, -x, 290)

            py5.stroke_weight(passo // 50 + py5.random(0.1, 1.1))
            py5.triangle(
                limite_x,
                limite_y,
                limite_x,
                limite_y - passo,
                limite_x - (passo / 1.5),
                limite_y,
            )

            py5.stroke_weight(passo // 50 + py5.random(0.1, 1.1))
            py5.rect(passo / 3.33, limite_y, x, -290)

        # Triangulos
        py5.stroke_weight(passo // 50 + py5.random(0.1, 1.1))
        py5.triangle(
            -limite_x,
            -limite_y + passo,
            -limite_x + (passo / 1.5),
            -limite_y + passo,
            -limite_x + (passo / 1.5),
            -limite_y,
        )
        py5.stroke_weight(passo // 50 + py5.random(0.1, 1.1))

        py5.triangle(
            limite_x,
            limite_y - passo,
            limite_x - (passo / 1.5),
            limite_y - passo,
            limite_x - (passo / 1.5),
            limite_y,
        )
        # Grandes retangulos
        incremento = 10
        y = 0
        py5.translate(4, 3, +80)
        while y < 290:
            y += incremento
            py5.stroke_weight(y // 49 + py5.random(0.1, 1.1))
            py5.rect(50 / 3.33, -limite_y, limite_x - (50 / 3.33), y)
            py5.stroke_weight(y // 49 + py5.random(0.1, 1.1))
            py5.rect(-50 / 3.33, limite_y, -limite_x + (50 / 3.33), -y)

    write_legend([py5.color(255)], img_name=IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
