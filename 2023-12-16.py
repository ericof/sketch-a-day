"""2023-12-16"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

n_seed = 9383
margem = -10
passo = 12
cor_base = 240
multiplicador = 0.02


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)


def draw():
    py5.noise_seed(n_seed)
    py5.fill(0)
    py5.rect(margem, margem, py5.width - margem * 2, py5.height - margem * 2)
    py5.color_mode(py5.HSB)
    f = 0  # use 'f = py5.frame_count' para versão animada
    x = margem
    while x < py5.width - margem:
        y = margem
        while y < py5.height - margem:
            h = 18 * py5.noise(
                x * multiplicador, (y + f) * multiplicador, f * multiplicador
            )
            py5.fill((cor_base + h * 4) % 255, 255, 255)
            largura = min(passo, h)
            py5.ellipse(x, y, largura, largura)
            y += h
        x += passo
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
