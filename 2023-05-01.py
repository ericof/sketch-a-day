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


def shape(xi, yi, xf, yf, largura, cor):
    largura = largura / 2
    noise = largura / 3
    xi0 = xi - largura
    xi1 = xi + largura
    xf0 = xf - largura
    xf1 = xf + largura
    py5.no_stroke()
    py5.fill(*cor)
    yi = int(yi)
    yf = int(yf)
    with py5.begin_shape():
        py5.vertex(xi0, yi)
        py5.vertex(xi1, yi)
        for y in range(yi, yf, -2):
            x = py5.random(-noise, noise) + xi1
            py5.vertex(x, y)
        py5.vertex(xf1, yf)
        py5.vertex(xf0, yf)
        for y in range(yf, yi, 2):
            x = py5.random(-noise, noise) + xf0
            py5.vertex(x, y)


def galho(y, tamanho, encurtamento, limite, atual=0):
    stroke_weight = tamanho / 10
    if stroke_weight < 1.2:
        cor = (0, 200, 0)
    else:
        cor = (66, 40, 14)
    shape(0, y, 0, y - tamanho, stroke_weight, cor)
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
    diametro = 10
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
