"""2023-04-28"""
from helpers import HEIGHT
from helpers import save_frame
from helpers import save_gif
from helpers import tmp_path
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

FUNDO = py5.color(248, 241, 219)

PATH = tmp_path()

FRAMES = []


def settings():
    py5.size(WIDTH, HEIGHT)


def setup():
    py5.background(FUNDO)
    py5.frame_rate(3)


def galho(y, tamanho, encurtamento, limite, atual=0):
    stroke_weight = tamanho / 10
    py5.stroke_weight(stroke_weight)
    if stroke_weight < 1.2:
        py5.stroke(0, 200, 0)
    else:
        py5.stroke(66, 40, 14)
    py5.line(0, y, 0, y - tamanho)
    atual += 1
    angulo = py5.radians(20)
    if atual < limite and tamanho > 5:
        encurtamento -= 0.01
        with py5.push_matrix():
            py5.translate(0, y - tamanho)
            py5.rotate(angulo)
            galho(
                0, (tamanho * encurtamento) - py5.random(3), encurtamento, limite, atual
            )
            py5.rotate(2 * -angulo)
            galho(
                0, (tamanho * encurtamento) - py5.random(3), encurtamento, limite, atual
            )


def draw():
    diametro = 0
    py5.background(FUNDO)
    write_legend(["#000000"], IMG_NAME)
    angulo = 30
    passos = 360 // angulo
    frame = py5.frame_count
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2)
        py5.rotate(py5.radians(frame))
        for passo in range(0, passos):
            tamanho = 80 if passo % 2 else 60
            encurtamento = 0.85 if passo % 2 else 0.95
            galho(-diametro, tamanho, encurtamento, limite=frame)
            py5.rotate(py5.radians(angulo))
    FRAMES.append(save_frame(PATH, IMG_NAME, frame))
    py5.window_title(f"FR: {py5.get_frame_rate():.1f} | Frame Count: {frame}")


def key_pressed():
    if py5.key == " ":
        py5.no_loop()
        print(f"Saving {len(FRAMES)} frames")
        save_gif(IMG_NAME, FRAMES, loop=None)
        py5.exit_sketch()


py5.run_sketch()
