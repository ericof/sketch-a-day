"""2023-08-31"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

from random import shuffle
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

# Fundo
FUNDO = py5.color(238, 243, 192)
PASSO = 10
DIAMETRO_FUNDO = PASSO // 2
DESLOCAMENTO = PASSO // 2

# Grade
MARGEM_X = 800
MARGEM_Y = 800
TAMANHO = 80
PONTOS = []


def elemento_fundo():
    s = py5.create_shape(py5.ELLIPSE, 0, 0, DIAMETRO_FUNDO, DIAMETRO_FUNDO * 1.5)
    s.set_stroke(False)
    s.set_fill(py5.color(220, 200, 220))
    return s


def desenha_fundo(cor):
    py5.background(cor)
    s = elemento_fundo()
    for idy, y in enumerate(range(-PASSO, HEIGHT + PASSO, PASSO)):
        deslocamento = DESLOCAMENTO if idy % 2 == 1 else 0
        for x0 in range(-PASSO, WIDTH + PASSO, PASSO):
            x = x0 + deslocamento
            py5.shape(s, x, y)


def poligono(ratio: float = 3) -> py5.Py5Shape:
    w = TAMANHO
    h = w * ratio
    s = py5.create_shape(py5.ELLIPSE, 0, 0, w, h)
    return s


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    desenha_fundo(FUNDO)
    for idy, y in enumerate(range(-MARGEM_Y, HEIGHT + MARGEM_Y, TAMANHO // 2)):
        buffer_x = 0 if idy % 2 else TAMANHO // 2
        for x in range(-MARGEM_X, WIDTH + MARGEM_X, TAMANHO):
            PONTOS.append((x + buffer_x, y))
    py5.shape_mode(py5.CENTER)
    py5.color_mode(py5.HSB, 360, 100, 100)
    ratio = 0.6
    forma = poligono(ratio=ratio)
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2)
        for angulo in range(0, 360, 120):
            py5.rotate(py5.radians(angulo))
            shuffle(PONTOS)
            for idx, (x, y) in enumerate(PONTOS):
                color = py5.color(abs(360 - idx), 30, 100, 50)
                forma.set_stroke(False)
                forma.set_fill(color)
                size_x = TAMANHO
                size_y = TAMANHO / ratio
                if idx % 2 == 0:
                    size_x, size_y = size_y, size_x
                py5.shape(forma, x, y, size_x, size_y)
    write_legend([py5.color(360, 0, 0)], img_name=IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
