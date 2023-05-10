"""2023-05-10"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from random import shuffle
from opensimplex import OpenSimplex


import py5

IMG_NAME = Path(__file__).name.replace(".py", "")

FUNDO = py5.color(226, 214, 187)

# Set up the OpenSimplex noise generator
noise_generator = OpenSimplex(seed=25624)


def par_bagunca(faixa_bagunca):
    bx = py5.random(-faixa_bagunca, faixa_bagunca)
    by = py5.random(-faixa_bagunca, faixa_bagunca)
    return bx, by


def caco(x, y, lado, faixa_bagunca):
    bx, by = par_bagunca(faixa_bagunca)
    x0, y0 = x - lado / 2 + bx, y - lado / 2 + by
    bx, by = par_bagunca(faixa_bagunca)
    x1, y1 = x + lado / 2 + bx, y - lado / 2 + by
    bx, by = par_bagunca(faixa_bagunca)
    x2, y2 = x + lado / 2 + bx, y + lado / 2 + by
    bx, by = par_bagunca(faixa_bagunca)
    x3, y3 = x - lado / 2 + bx, y + lado / 2 + by
    s = py5.create_shape()
    with s.begin_closed_shape():
        s.vertex(x0, y0)
        s.vertex(x1, y1)
        s.vertex(x2, y2)
        s.vertex(x3, y3)
    return s


def margem(margem_x, margem_y):
    py5.no_stroke()
    py5.fill(FUNDO)
    py5.rect(0, 0, WIDTH, margem_y)
    py5.rect(WIDTH - margem_x, 0, WIDTH, HEIGHT)
    py5.rect(0, HEIGHT - margem_y, WIDTH, HEIGHT)
    py5.rect(0, 0, margem_x, HEIGHT)


def setup():
    py5.size(WIDTH, HEIGHT)
    py5.color_mode(py5.RGB)
    py5.background(FUNDO)
    py5.stroke(py5.color(180))
    margem_x = 70
    margem_y = 40
    pontos = []
    for y0 in range(margem_x - 10, HEIGHT, 30):
        for x0 in range(margem_y - 10, WIDTH, 30):
            noise = noise_generator.noise2(x0, y0)
            y = y0 + (15 * noise)
            x = x0 + (15 * noise)
            stroke = py5.random_int(1, 3)
            pontos.append((x, y, stroke))
    shuffle(pontos)
    for idx, (x, y, stroke) in enumerate(pontos):
        cor = py5.color(152, 59, 47)
        if idx % 5 == 0:
            cor = py5.color(0)
        elif idx % 7 == 0:
            cor = py5.color(218, 160, 57)
        s = caco(0, 0, 20, 5)
        s.set_stroke_weight(stroke)
        s.set_fill(cor)
        lado = py5.random_int(20, 25)
        py5.shape(s, x, y, lado, lado)
    # Desenha margem
    margem(margem_x, margem_y)
    write_legend([py5.color(0)], img_name=IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
