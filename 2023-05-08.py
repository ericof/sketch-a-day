"""2023-05-08"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import cv2
import py5

IMG_NAME = Path(__file__).name.replace(".py", "")


movie = cv2.VideoCapture(0)


def setup():
    py5.size(WIDTH, HEIGHT)


def draw():
    py5.background(py5.color(248, 241, 219))
    success, frame = movie.read()  # frame is a numpy array
    tamanho_pixel = 10
    limite_quant = 250
    buffer_x = len(frame[0]) - py5.width
    buffer_y = len(frame) - py5.height
    py5.ellipse_mode(py5.CENTER)
    py5.fill(py5.color(20, 20, 20))
    if success:
        frame = cv2.cvtColor(
            frame[::tamanho_pixel, ::tamanho_pixel], cv2.COLOR_BGR2GRAY
        )
        for y0, line in enumerate(frame):
            y = y0 * tamanho_pixel - buffer_y + tamanho_pixel
            for x0, col in enumerate(line):
                x = x0 * tamanho_pixel - buffer_x + tamanho_pixel
                size = tamanho_pixel - ((col / limite_quant) * tamanho_pixel)
                py5.circle(x, y, size)

    write_legend([py5.color(255)], img_name=IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
