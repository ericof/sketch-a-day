"""2023-12-26"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from random import shuffle

import numpy as np
import opensimplex
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

noise_generator = opensimplex.seed(39874)
noise_scale = 0.015
time_speed = [0.2, 4.0]
h_range = [(270, 300), (255, 285), (240, 270), (225, 255), (210, 240)]
passo_x = 5
passo_y = 3
forma_x = (3, 5)
forma_y = (4, 6)
NIVEIS = len(h_range)
PROFUNDIDADE = 20
VELOCIDADE = 80
PONTOS = []
TOTAL = 0
FORMA = None


def setup():
    global FORMA
    global PONTOS
    global TOTAL
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.shape_mode(py5.CENTER)
    py5.no_stroke()
    FORMA = py5.create_shape(py5.RECT, 0, 0, 10, 10)
    time = np.array([py5.millis() * py5.random(*time_speed) for _ in range(NIVEIS)])
    X = np.arange(0, WIDTH, passo_x)
    Y = np.arange(0, HEIGHT, passo_y)
    XN = np.array([x * noise_scale for x in X])
    YN = np.array([y * noise_scale for y in Y])
    noise_val = opensimplex.noise3array(XN, YN, time)
    s = 100
    b = 100
    t_passo = 75 // NIVEIS
    PONTOS = []
    for idx, x in enumerate(X):
        for idy, y in enumerate(Y):
            pontos = []
            for idz in range(0, NIVEIS):
                noise = noise_val[idz][idy][idx]
                z = idz * PROFUNDIDADE
                h = int(py5.remap(noise, -1, 1, *h_range[idz]))
                t = 100 - (idz * t_passo)
                largura = int(py5.remap(noise, -1, 1, *forma_x))
                altura = int(py5.remap(noise, -1, 1, *forma_y))
                pontos.append((x, y, z, py5.color(h, s, b, t), largura, altura))
            PONTOS.append(pontos)
    shuffle(PONTOS)
    TOTAL = len(PONTOS)


def draw():
    frame = py5.frame_count
    initial = frame * VELOCIDADE
    final = initial + VELOCIDADE
    final = TOTAL if final >= TOTAL else final
    concluido = final / TOTAL
    for i in range(initial, final):
        for nivel in range(NIVEIS):
            x, y, z, cor, largura, altura = PONTOS[i][nivel]
            with py5.push_matrix():
                py5.translate(x, y, z)
                FORMA.set_fill(cor)
                py5.shape(FORMA, 0, 0, largura, altura)
    py5.window_title(
        f"FR: {py5.get_frame_rate():.1f} | Frame Count: {frame} | {concluido*100:0.02f}%"
    )
    write_legend([py5.color(360, 0, 100)], IMG_NAME)
    if concluido >= 1:
        save_and_close()


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
