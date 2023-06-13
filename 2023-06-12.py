"""2023-06-12"""
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
forma = None


LIMITES = [650, 700, 725, 750, 750, 725, 700, 650]


def criar_forma(pontos):
    forma = py5.create_shape()
    with forma.begin_closed_shape():
        # forma.no_fill()
        for x, y in pontos:
            forma.vertex(x, y)
    return forma


def setup():
    global forma
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.stroke_weight(2)
    py5.frame_rate(1)
    pontos = []
    for t in range(-400, 400):
        x = 16 * (np.sin(t)) ** 3
        y = (
            (13 * np.cos(t))
            - (5 * np.cos(2 * t))
            - (2 * np.cos(3 * t))
            - (np.cos(4 * t))
        )
        pontos.append((x, -y))
    forma = criar_forma(pontos)


def draw():
    frame = py5.frame_count
    lista_indice = frame % 8 - 1 if frame % 8 else 7
    limite = LIMITES[lista_indice]
    print(frame, lista_indice, limite)
    py5.background(0)
    with py5.push_matrix():
        py5.translate(WIDTH / 2, (HEIGHT / 2) - 50)
        o = 10
        for idx in range(limite, 50, -25):
            color = py5.color(255, 0, 0, o)
            forma.set_stroke(color)
            forma.set_stroke_weight(1)
            forma.set_fill(color)
            py5.shape(forma, 0, 0, idx, idx)
            o += 10
    write_legend([py5.color(255)], IMG_NAME)
    FRAMES.append(save_frame(PATH, IMG_NAME, frame))
    if frame >= 8:
        py5.no_loop()
    py5.window_title(f"FR: {py5.get_frame_rate():.1f} | Frame Count: {frame}")


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_gif(IMG_NAME, FRAMES, duration=100)
        py5.exit_sketch()


py5.run_sketch()
