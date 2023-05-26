"""2023-05-26"""
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

FRAMES = []

CIRCULOS = []
PASSO = -4


def calcula_circulo(diametro, z):
    raio = diametro / 2
    n = int(raio)
    pontos = []
    for ponto in range(0, n + 1):
        x = np.cos(2 * py5.PI / n * ponto) * raio
        y = np.sin(2 * py5.PI / n * ponto) * raio
        pontos.append((int(x), int(y), z))
    return pontos


def popula_esfera(max_diametro=720, min_diametro=10):
    esfera = []
    passo = PASSO
    for direcao in (-1, 1):
        z = 0
        for diametro in range(max_diametro, min_diametro, passo):
            esfera.append(calcula_circulo(diametro, z))
            z += passo * direcao
    return esfera


def setup():
    global CIRCULOS
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.frame_rate(5)
    CIRCULOS = popula_esfera(720)


def draw():
    py5.background(22, 0, 0)
    write_legend([py5.color(100)], IMG_NAME)
    frame = py5.frame_count
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2, 50)
        for idx, circulo in enumerate(CIRCULOS):
            py5.stroke(py5.color(idx / 2, 100, 90))
            with py5.begin_shape():
                for idy, (x, y, z) in enumerate(circulo):
                    if idy % 4 != 1:
                        continue
                    xyz = x, y, z
                    z1 = int(z * 0.7) + 1
                    z2 = -z1
                    z_range = sorted([z2, z1])
                    z_f = py5.random_int(*z_range)
                    py5.vertex(x, y, z_f)
    if frame % 4 == 1:
        FRAMES.append(save_frame(PATH, IMG_NAME, frame))
    if len(FRAMES) > 45:
        print("Too many frames")
        py5.no_loop()
    py5.window_title(f"FR: {py5.get_frame_rate():.1f} | Frame Count: {frame}")


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_gif(IMG_NAME, FRAMES, duration=100)
        py5.exit_sketch()


py5.run_sketch()
