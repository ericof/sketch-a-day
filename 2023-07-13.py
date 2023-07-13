"""2023-07-13"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5

IMG_NAME = Path(__file__).name.replace(".py", "")


def sorteia_cor():
    return py5.color(30, py5.random(22, 90), py5.random(50, 75))


def triangles(x, y, largura):
    color = sorteia_cor()
    py5.stroke(color)
    py5.fill(color)
    metade = largura / 2
    x0 = x
    x1 = x - metade
    x2 = x + metade
    x3 = x2 + metade
    y0 = y
    y1 = y + largura
    with py5.begin_shape():
        py5.vertex(x1, y0)
        py5.vertex(x2, y0)
        py5.vertex(x0, y1)
        py5.vertex(x1, y0)
    color = sorteia_cor()
    py5.stroke(color)
    py5.fill(color)
    with py5.begin_shape():
        py5.vertex(x0, y1)
        py5.vertex(x3, y1)
        py5.vertex(x2, y0)
        py5.vertex(x0, y1)


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    buffer = 4
    largura = HEIGHT // 40
    linhas = HEIGHT + (buffer * largura) // largura
    colunas = HEIGHT + (buffer * largura) // largura
    buffer_linha = py5.random(buffer / 2, buffer) * largura
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2)
        py5.rotate(py5.radians(35))
        for i in range(linhas):
            y = i * largura - buffer_linha
            buffer_coluna = py5.random(buffer / 2, buffer) * largura
            func = triangles
            for j in range(colunas):
                x = j * largura - buffer_coluna
                func(x - WIDTH, y - HEIGHT, largura)
    write_legend(img_name=IMG_NAME)
    save_image(IMG_NAME, "png")


py5.run_sketch()
