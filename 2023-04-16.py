"""2023-04-16"""
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

FRAMES = []


def settings():
    py5.size(WIDTH, HEIGHT)


def setup():
    py5.background("#000000")
    py5.no_stroke()
    py5.shape_mode(py5.CENTER)
    write_legend(["#FFFFFF"], IMG_NAME)
    py5.frame_rate(10)
    py5.color_mode(py5.HSB)


def draw():
    margem = 100
    linhas = 20
    colunas = 20
    lado = (WIDTH - margem * 2) / colunas
    espacamento = 8
    lado_interno = lado - espacamento
    frame_count = py5.frame_count
    frame = frame_count % 100 if frame_count < 100 else 100 - (frame_count % 100)
    top = frame % 10 if int(frame / 10) % 2 else 10 - (frame % 10)
    limit = [i for i in range(0, top)] + [19 - i for i in range(0, top)]
    if frame_count != frame and frame == 1:
        py5.no_loop()
        save_gif(IMG_NAME, FRAMES)
        py5.exit_sketch()
    else:
        print(frame)
        py5.background("#000000")
        write_legend(["#FFFFFF"], IMG_NAME)
        for j in range(linhas):
            for i in range(colunas):
                x = margem + lado / 2 + i * lado
                y = margem + lado / 2 + j * lado
                ceiling = 200
                base_h = py5.random(abs(py5.cos(frame * 1) * i * 10), 255)
                base_s = py5.random((20 - len(limit)) * 10, 255)
                if i % colunas in limit or j % colunas in limit:
                    continue
                elif frame < 10:
                    ceiling = 120
                color = py5.color(
                    base_h,
                    base_s,
                    py5.random(100, ceiling),
                )
                shape = bandeirola(color, i)
                py5.shape(shape, x, y, lado_interno, lado_interno)
        # Save only half of the frames
        if frame_count % 2:
            FRAMES.append(save_frame(PATH, IMG_NAME, frame_count))


def bandeirola(color, i) -> py5.SHAPE:
    x = 10
    y = 10
    lado = 20
    dance = py5.random(i % 4)
    min_x = x - (lado / 2)
    min_y = y - (lado / 2)
    max_x = x + (lado / 2)
    max_y = y + (lado / 2)
    med_x = x
    med_y = y + (lado / 4)
    s = py5.create_shape()
    with s.begin_closed_shape():
        s.fill(color)
        s.vertex(min_x, min_y)
        s.vertex(max_x, min_y)
        s.vertex(max_x, max_y)
        s.vertex(med_x + dance, med_y)
        s.vertex(min_x + dance, max_y)
    return s


py5.shape
py5.run_sketch()
