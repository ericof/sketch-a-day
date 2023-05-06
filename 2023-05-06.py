"""2023-05-06"""
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

INICIO = 2
DIAMETRO = 700
PONTOS = []

COR_H = 40
COR_S = 100
COR_B = 100
COR_A = 100

BUFFER = 290


def calcula_circulo(diametro):
    raio = diametro // 2
    n = 360
    for ponto in range(0, n + 1):
        x = np.cos(2 * py5.PI / n * ponto) * raio
        y = np.sin(2 * py5.PI / n * ponto) * raio
        PONTOS.append((int(x), int(y)))


def setup():
    py5.size(WIDTH, HEIGHT, py5.P2D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(0)
    calcula_circulo(DIAMETRO)
    py5.frame_rate(1)


def draw():
    frame = py5.frame_count
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2)
        vertices = INICIO + frame
        angle = 360 / vertices
        h = vertices * 15
        s = COR_S
        b = COR_B
        a = COR_A - 15 * (frame)
        if a < 20:
            a = 20
        buffer = abs(BUFFER - 20 * (frame))
        py5.stroke(360, 0, 100)
        py5.fill(h, s, b, a)
        with py5.begin_shape():
            for i in range(0, vertices + 1):
                if (idx := int(i * angle) + buffer) > 360:
                    idx = idx % 360
                x, y = PONTOS[idx]
                py5.vertex(x, y)
        buffer -= 20
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
