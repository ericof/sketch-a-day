"""2023-08-06"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

FUNDO = py5.color(238, 243, 192)

PASSO = 10
DIAMETRO_FUNDO = PASSO // 2
DESLOCAMENTO = PASSO // 2

MARGEM_X = 600
MARGEM_Y = 600
TAMANHO = 80
PONTOS = []


def elemento_fundo():
    s = py5.create_shape(py5.ELLIPSE, 0, 0, DIAMETRO_FUNDO, DIAMETRO_FUNDO)
    s.set_stroke(False)
    s.set_fill(py5.color(209, 212, 181))
    return s


def desenha_fundo(cor):
    py5.background(cor)
    s = elemento_fundo()
    for idy, y in enumerate(range(-PASSO, HEIGHT + PASSO, PASSO)):
        deslocamento = DESLOCAMENTO if idy % 2 == 1 else 0
        for x0 in range(-PASSO, WIDTH + PASSO, PASSO):
            x = x0 + deslocamento
            py5.shape(s, x, y)


def poligono() -> py5.Py5Shape:
    s = py5.create_shape(py5.ELLIPSE, 0, 0, 80, 40)
    return s


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    for idy, y in enumerate(range(-MARGEM_Y, HEIGHT + MARGEM_Y, TAMANHO // 2)):
        buffer_x = 0 if idy % 2 else TAMANHO // 2
        for x in range(-MARGEM_X, WIDTH + MARGEM_X, TAMANHO):
            PONTOS.append((x + buffer_x, y))
    desenha_fundo(FUNDO)
    py5.shape_mode(py5.CENTER)
    forma = poligono()
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2)
        for angulo in range(0, 360, 15):
            py5.rotate(py5.radians(angulo))
            for idx, (x, y) in enumerate(PONTOS):
                weight = idx % 2 + 1
                forma.set_stroke(py5.color(200, 50, angulo / 15))
                forma.set_stroke_weight(weight)
                forma.set_fill(False)
                py5.shape(forma, x, y, TAMANHO, TAMANHO)
    write_legend([py5.color(100)], img_name=IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()