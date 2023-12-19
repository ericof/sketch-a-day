"""2023-12-19"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

n_seed = 1975
margem = -50
passo = 19
cor_base = 12
multiplicador = 0.015


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
        idy = 0
        while y < py5.height - margem:
            buffer = 0
            h_base = cor_base
            if idy % 2:
                h_base = cor_base * 1.3
                buffer = passo * 0.5
            h = 18 * py5.noise(
                x * multiplicador, (y + f) * multiplicador, f * multiplicador
            )
            py5.fill((h_base + h * 4) % 255, 255, 255)
            largura = min(passo, h)
            py5.ellipse(x + buffer, y, largura, largura)
            y += h
            idy += 1
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
