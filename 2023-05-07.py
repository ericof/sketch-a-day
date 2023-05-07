"""2023-05-05"""
from helpers import HEIGHT
from helpers import save_frame
from helpers import save_gif
from helpers import tmp_path
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path


import numpy as np
import py5

IMG_NAME = Path(__file__).name.replace(".py", "")
PATH = tmp_path()

DIAMETRO = 700
PONTOS = []
FRAMES = []


def sorteia_cor(base: int):
    return py5.color(base, py5.random(22, 90), py5.random(50, 75))


def dentro_circulo(circulo_x, circulo_y, raio, x, y, largura):
    x0 = x
    x1 = x + largura
    y0 = y
    y1 = y + largura
    pontos = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    for x, y in pontos:
        if (x - circulo_x) * (x - circulo_x) + (y - circulo_y) * (
            y - circulo_y
        ) <= raio * raio:
            continue
        else:
            return False
    return True


def square(x, y, largura, cor):
    py5.stroke(cor)
    py5.fill(cor)
    x0 = x
    x1 = x + largura
    y0 = y
    y1 = y + largura
    py5.quad(x0, y0, x1, y0, x1, y1, x0, y1)


def setup():
    py5.size(WIDTH, HEIGHT)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.frame_rate(3)


def draw():
    frame = py5.frame_count
    py5.background(0, 0, 0)
    buffer = 4
    largura = HEIGHT // (frame * 10)
    linhas = HEIGHT + (buffer * largura) // largura
    colunas = HEIGHT + (buffer * largura) // largura
    buffer_linha = py5.random(buffer / 2, buffer) * largura
    for i in range(linhas):
        y = i * largura - buffer_linha
        buffer_coluna = py5.random(buffer / 2, buffer) * largura
        func = square
        for j in range(colunas):
            x = j * largura - buffer_coluna
            if dentro_circulo(400, 400, 300, x, y, largura):
                cor = sorteia_cor((frame % 18) * 20)
                func(x, y, largura, cor)
    py5.window_title(f"FR: {py5.get_frame_rate():.1f} | Frame Count: {frame}")
    write_legend([py5.color(360, 0, 100)], img_name=IMG_NAME)
    FRAMES.append(save_frame(PATH, IMG_NAME, frame))


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_gif(IMG_NAME, FRAMES)
        py5.exit_sketch()


py5.run_sketch()
