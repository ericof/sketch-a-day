"""2023-05-14"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import cv2
import py5

IMG_NAME = Path(__file__).name.replace(".py", "")


movie = cv2.VideoCapture(0)
tamanho_pixel = 10
buffer_x = 1920 / 2 - WIDTH / 2
buffer_y = 1080 / 2 - HEIGHT / 2


def reticula():
    s = py5.create_shape()
    with s.begin_closed_shape():
        s.vertex(30, 0)
        s.vertex(60, 0)
        s.vertex(90, 30)
        s.vertex(90, 60)
        s.vertex(60, 90)
        s.vertex(30, 90)
        s.vertex(0, 60)
        s.vertex(0, 30)
    return s


def setup():
    py5.size(WIDTH, HEIGHT)


def draw():
    global tamanho_pixel, buffer_x, buffer_y
    py5.background(py5.color(248, 241, 219))
    success, frame = movie.read()  # frame is a numpy array
    color_limit = 255
    color_quant = color_limit / tamanho_pixel
    limite_quant = 250
    py5.ellipse_mode(py5.CENTER)
    if success:
        frame = cv2.cvtColor(
            frame[::tamanho_pixel, ::tamanho_pixel], cv2.COLOR_BGR2GRAY
        )
        for y0, line in enumerate(frame):
            y = y0 * tamanho_pixel - buffer_y + tamanho_pixel
            for x0, col in enumerate(line):
                x = x0 * tamanho_pixel - buffer_x + tamanho_pixel
                size = tamanho_pixel - ((col / limite_quant) * tamanho_pixel)
                color = py5.color(color_limit - (color_quant * size))
                s = reticula()
                s.set_stroke(color)
                s.set_fill(color)
                py5.shape(s, x, y, size, size)

    write_legend([py5.color(color_limit)], img_name=IMG_NAME)


def key_pressed():
    global tamanho_pixel
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, "png")
        py5.exit_sketch()
    elif py5.key_code == 38:
        print(tamanho_pixel)
        tamanho_pixel += 1
    elif py5.key_code == 40:
        print(tamanho_pixel)
        tamanho_pixel -= 1


py5.run_sketch()
