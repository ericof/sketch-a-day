"""2023-08-03"""
from helpers import HEIGHT
from helpers import save_frame
from helpers import save_gif
from helpers import tmp_path
from helpers import WIDTH
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")
PATH = tmp_path()
FRAMES = []

FUNDO = py5.color(0)

largura = 20


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(0)
    py5.frame_rate(4)


def draw():
    global largura
    frame = py5.frame_count
    py5.stroke(219, 172, 52)
    py5.stroke_weight(2)
    py5.no_fill()
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2, -800)
        if frame % 2 == 0:
            pontos = [
                (-largura / 2, -largura / 2),
                (largura / 2, -largura / 2),
                (largura / 2, largura / 2),
                (-largura / 2, largura / 2),
            ]
            largura = largura * 2
        else:
            pontos = [
                (0, -largura / 2),
                (largura / 2, 0),
                (0, largura / 2),
                (-largura / 2, 0),
            ]
        z = 0
        with py5.begin_closed_shape():
            for x, y in pontos:
                py5.vertex(x, y, z)

    FRAMES.append(save_frame(PATH, IMG_NAME, frame))
    if largura <= 10:
        py5.no_loop()

    py5.window_title(f"FR: {py5.get_frame_rate():.1f} | Frame Count: {frame}")


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_gif(IMG_NAME, FRAMES, duration=0.5)
    py5.exit_sketch()


py5.run_sketch()
