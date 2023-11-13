"""2023-11-13"""
from helpers import HEIGHT
from helpers import save_frame
from helpers import save_gif
from helpers import tmp_path
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from py5 import create_image_from_numpy
from random import shuffle

import cv2
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")
PATH = tmp_path()

movie = cv2.VideoCapture(0)

MARGEM = 50
LINHAS = 10
ALTURA = HEIGHT - (MARGEM * 2)
LADO = int(ALTURA / LINHAS)

FRAMES = []

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
    success, frame = movie.read()  # frame is a numpy array
    frame_id = py5.frame_count
    py5_img = None
    py5.shape_mode(py5.CORNERS)
    # Shuffle only after a while
    if frame_id > 1:
        shuffle(SLOTS)
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
                forma = py5.create_shape(py5.RECT, 0, 0, LADO, LADO)
                forma.set_texture(py5_img)
                forma.set_stroke(py5.color(0, 100, 100))
                forma.set_stroke_weight(100)
                slot = SLOTS[slot_id]
                py5.shape(forma, *slot)
                slot_id += 1
    write_legend([py5.color(360, 0, 100)], IMG_NAME)
    FRAMES.append(save_frame(PATH, IMG_NAME, frame_id))
    if frame_id == 4:
        _end()


def _end():
    py5.no_loop()
    save_gif(IMG_NAME, FRAMES, duration=0.5)
    py5.exit_sketch()


def key_pressed():
    key = py5.key
    if key == " ":
        _end()


py5.run_sketch()
