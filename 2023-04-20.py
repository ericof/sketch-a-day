"""2023-04-20"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

overlap = 0.86


def settings():
    py5.size(WIDTH, HEIGHT)


def setup():
    background()
    write_legend(["#FFFFFF"], IMG_NAME)
    py5.color_mode(py5.HSB, 300)
    circles()
    save_image(IMG_NAME, "png")


def background():
    py5.background(0)


def circles():
    global overlap
    pontos = []
    margem = 80
    linhas = [(0, 3), (4, 3), (1, 4), (3, 4), (2, 5)]
    num_linhas = len(linhas)
    diametro = (WIDTH - margem * 2) / (num_linhas - 2)
    raio = diametro / 2
    py5.no_fill()
    for i in range(0, 40, 2):
        py5.stroke(i * 5 + 50, 200, 80)
        py5.circle(400, 370, py5.height - (margem * 2) + (i * 3))
    for j, idx in linhas:
        start = num_linhas - idx - 1 if idx < num_linhas else 0
        finish = start + idx
        for i in range(start, finish):
            indent = (j % 2) * (raio / 2)
            x = (margem + raio) + (i * raio) + indent
            y = (margem + raio) + (j * raio * overlap)
            alpha = 95  # idx * 20
            base_h = py5.random(idx * 20, 300)
            base_s = py5.random(idx + 180, 300)
            py5.fill(base_h, base_s, 250, alpha)
            py5.stroke(base_h, base_s, 180, alpha + 20)
            py5.circle(x, y, diametro)
            pontos.append((x, y))
    for x, y in pontos:
        py5.fill(0, 0, 0)
        py5.circle(x, y, 3)


py5.run_sketch()
