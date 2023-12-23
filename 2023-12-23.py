"""2023-12-23"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

n_seed = 80
margem = -90
passo = 4
cor_base = 240
multiplicador = 0.012


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)


def draw():
    py5.noise_seed(n_seed)
    py5.fill(0)
    py5.rect(margem, margem, py5.width - margem * 2, py5.height - margem * 2)
    py5.color_mode(py5.HSB)
    f = 3
    y = margem
    while y < py5.height - margem:
        x = margem
        idx = 0
        while x < py5.width - margem:
            buffer = 0
            h_base = cor_base
            if idx % 2 == 0:
                h_base = cor_base * 1.2
                buffer = passo * 0.6
            h = 22 * py5.noise(
                (x + f) * multiplicador, y * multiplicador, f * multiplicador
            )
            py5.fill((h_base + h * 3) % 255, 255, 255)
            largura = min(passo, h)
            py5.ellipse(x, y + buffer, largura, largura)
            x += h
            idx += 1
        y += passo
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
