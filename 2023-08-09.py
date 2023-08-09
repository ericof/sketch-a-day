"""2023-08-09"""
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
MARGEM_X = 300
MARGEM_Y = 300
TAMANHO = 50
PONTOS = []


def elemento_fundo():
    s = py5.create_shape(py5.ELLIPSE, 0, 0, DIAMETRO_FUNDO / 2, DIAMETRO_FUNDO)
    s.set_stroke(False)
    s.set_fill(py5.color(80, 80, 80))
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
    h = TAMANHO
    w = h / ratio
    s = py5.create_shape(py5.ELLIPSE, 0, 0, w, h)
    return s


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    desenha_fundo(FUNDO)
    for idy, y in enumerate(range(-MARGEM_Y, HEIGHT + MARGEM_Y, TAMANHO // 2)):
        buffer_x = 0 if idy % 2 else TAMANHO // 2
        for x in range(-MARGEM_X, WIDTH + MARGEM_X, TAMANHO):
            PONTOS.append((x + buffer_x, y))
    shuffle(PONTOS)
    py5.shape_mode(py5.CENTER)
    py5.color_mode(py5.HSB, 360, 100, 100)
    forma = poligono(ratio=4.5)
    z = 0
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2, z)
        for angulo in range(0, 360, 20):
            py5.rotate(py5.radians(angulo))
            for idx, (x, y) in enumerate(PONTOS):
                weight = 1
                h = 200 - (idx // 2)
                if -50 <= y <= 50:
                    weight = 2
                color = py5.color(h, 80, 90)
                forma.set_stroke(color)
                forma.set_stroke_weight(weight)
                forma.set_fill(False)
                py5.shape(forma, x, y, TAMANHO, TAMANHO)
    write_legend([py5.color(0)], img_name=IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
