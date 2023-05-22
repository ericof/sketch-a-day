"""2023-05-22"""
from helpers import HEIGHT
from helpers import save_frame
from helpers import save_gif
from helpers import tmp_path
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")
PATH = tmp_path()


FUNDO = py5.color(248, 241, 219)

FRAMES = []

MARGEM_X = 200
MARGEM_Y = 200
TAMANHO = 80
TAMANHO_I = 4
PONTOS = []


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.frame_rate(15)
    for idy, y in enumerate(range(-MARGEM_Y, HEIGHT + MARGEM_Y, TAMANHO // 2)):
        buffer_x = 0 if idy % 2 else TAMANHO // 2
        for x in range(-MARGEM_X, WIDTH + MARGEM_X, TAMANHO):
            PONTOS.append((x + buffer_x, y))


def draw():
    py5.background(FUNDO)
    py5.color_mode(py5.HSB, 100, 100, 100)
    py5.shape_mode(py5.CENTER)
    write_legend([py5.color(0)], img_name=IMG_NAME)
    forma = py5.create_shape(py5.ELLIPSE, 0, 0, 20, 20)
    frame = py5.frame_count
    tamanho = TAMANHO_I + frame
    for x, y in PONTOS:
        h = abs((y // 400 * 400) - (y % 400)) / 4
        b = abs((x // 420 * 420) - (x % 420)) / 4
        cor = py5.color(h, b, 60, 40)
        cor_stroke = py5.color(h, b + 10, 100, 80)
        forma.set_stroke_weight(2)
        forma.set_stroke(cor_stroke)
        forma.set_fill(cor)
        py5.shape(forma, x, y, tamanho, tamanho)
    if frame % 3 == 1:
        FRAMES.append(save_frame(PATH, IMG_NAME, frame))
    py5.window_title(f"FR: {py5.get_frame_rate():.1f} | Frame Count: {frame}")


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_gif(IMG_NAME, FRAMES, duration=100)
        py5.exit_sketch()


py5.run_sketch()
