"""2023-09-01"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from random import choice

import numpy as np
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

PIXELS = []
VERTICES = []


def calcula_circulo(diametro):
    pontos = []
    raio = diametro // 2
    n = 360
    for ponto in range(0, n + 1):
        x = np.cos(2 * py5.PI / n * ponto) * raio
        y = np.sin(2 * py5.PI / n * ponto) * raio
        pontos.append((int(x) + 400, int(y) + 400))
    return pontos


def poligono(pontos, lados=3):
    angle = 360 / lados
    s = py5.create_shape()
    with s.begin_closed_shape():
        for i in range(0, lados + 1):
            if (idx := int(i * angle)) > 360:
                idx = idx % 360
            x, y = pontos[idx]
            x = x if x != 201 else 200
            color = (
                idx,
                100,
                100,
            )
            VERTICES.append((x, y, color))
            print((x, y, color))
            s.vertex(x, y)
    return s


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(py5.color(248, 241, 219))
    write_legend([py5.color(0)], IMG_NAME)
    pontos = calcula_circulo(800)
    py5.shape_mode(py5.CORNERS)
    lados = 6
    forma = poligono(pontos, lados)
    cor = py5.color(0)
    forma.set_stroke(cor)
    forma.set_stroke_weight(1)
    forma.set_fill(cor)
    py5.shape(forma, 0, 0)
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            c = py5.get_pixels(x, y)
            if c == cor:
                PIXELS.append((x, y))
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(py5.color(0))


def draw():
    frame = py5.frame_count
    inside = False
    while not inside:
        x0 = py5.random_int(0, WIDTH)
        y0 = py5.random_int(0, HEIGHT)
        inside = True if (x0, y0) in PIXELS else False
    x1, y1, color = choice(VERTICES)
    xa = np.linspace(x0, x1, 1000)
    ya = np.linspace(y0, y1, 1000)
    x = xa[666]
    y = ya[666]
    py5.stroke(py5.color(*color))
    py5.stroke_weight(2)
    py5.point(x, y)
    py5.window_title(f"FR: {py5.get_frame_rate():.1f} | Frame Count: {frame}")


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
