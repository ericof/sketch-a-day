"""2023-11-18"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from py5 import create_image_from_numpy

import cv2
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

movie = cv2.VideoCapture(0)

MARGEM = 50
LINHAS = 20
ALTURA = HEIGHT - (MARGEM * 2)
LADO = int(ALTURA / LINHAS)

SLOTS = []


def centered_frame(base_frame):
    frame_height, frame_width = len(base_frame), len(base_frame[0])
    buffer_h = (frame_height - ALTURA) // 2
    buffer_w = (frame_width - ALTURA) // 2
    frame = base_frame[
        buffer_h : frame_height - buffer_h, buffer_w : frame_width - buffer_w
    ]
    return frame


def background():
    py5.background(py5.color(360, 0, 0))


def setup():
    global SLOTS
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.no_smooth()
    py5.frame_rate(1)
    py5.color_mode(py5.HSB, 360, 100, 100)
    background()
    for y0 in range(MARGEM, HEIGHT - MARGEM, LADO):
        y1 = y0 + LADO
        for x0 in range(MARGEM, WIDTH - MARGEM, LADO):
            x1 = x0 + LADO
            SLOTS.append((x0, y0, x1, y1))


def draw():
    global py5_img
    background()
    success, frame = movie.read()  # frame is a numpy array
    py5_img = None
    py5.shape_mode(py5.CORNERS)
    if success:
        py5.lights()
        py5.no_stroke()
        new_frame = centered_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA))
        max_y, max_x = len(new_frame), len(new_frame[0])
        slot_id = 0
        for y0 in range(0, max_y, LADO):
            y1 = y0 + LADO
            for x0 in range(0, max_x, LADO):
                x1 = x0 + LADO
                partial = new_frame[y0:y1, x0:x1]
                py5_img = create_image_from_numpy(partial, "RGBA", dst=py5_img)
                forma = py5.create_shape(py5.ELLIPSE, 0, 0, LADO, LADO)
                forma.set_texture(py5_img)
                forma.set_texture_mode(py5.NORMAL)
                a0 = int(
                    (x0 / WIDTH) * py5.random_int(30)
                    + (y0 / HEIGHT) * py5.random_int(10)
                )
                a1 = int(a0 * 1.10)
                angulo = py5.random_int(a0, a1)
                forma.rotate(py5.radians(angulo))
                slot = SLOTS[slot_id]
                py5.shape(forma, *slot)
                slot_id += 1
    write_legend([py5.color(360, 0, 100)], IMG_NAME)


def _end():
    py5.no_loop()
    save_image(IMG_NAME, extension="png")
    py5.exit_sketch()


def key_pressed():
    key = py5.key
    if key == " ":
        _end()


py5.run_sketch()
