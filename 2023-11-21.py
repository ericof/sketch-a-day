"""2023-11-21"""
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
LINHAS = 4
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


def frame_slice(frame, x0, y0, x1, y1):
    partial = frame[y0:y1, x0:x1]
    return create_image_from_numpy(partial, "RGBA")


def background():
    py5.background(py5.color(360, 0, 0))


def cria_forma(largura: int, imagem):
    A = (
        (-1, -1, 1, 0, 0),  # +Z "front" face.
        (1, -1, 1, 1, 0),
        (1, 1, 1, 1, 1),
        (-1, 1, 1, 0, 1),
    )
    B = (
        (-1, -1, -1, 0, 0),  # -Z "back" face.
        (1, -1, -1, 1, 0),
        (1, -1, 1, 1, 1),
        (-1, -1, 1, 0, 1),
    )
    C = (
        (1, -1, -1, 0, 0),  # +Y "bottom" face.
        (-1, -1, -1, 1, 0),
        (-1, 1, -1, 1, 1),
        (1, 1, -1, 0, 1),
    )
    D = (
        (-1, 1, 1, 0, 0),  # -Y "top" face.
        (1, 1, 1, 1, 0),
        (1, 1, -1, 1, 1),
        (-1, 1, -1, 0, 1),
    )
    E = (
        (1, -1, 1, 0, 0),  # +X "right" face.
        (1, -1, -1, 1, 0),
        (1, 1, -1, 1, 1),
        (1, 1, 1, 0, 1),
    )
    F = (
        (-1, -1, -1, 0, 0),  # -X "left" face.
        (-1, -1, 1, 1, 0),
        (-1, 1, 1, 1, 1),
        (-1, 1, -1, 0, 1),
    )
    tc = py5.create_shape(py5.GROUP)
    tc.scale(largura)
    for idx, face in enumerate((A, B, C, D, E, F)):
        tf = py5.create_shape()
        with tf.begin_shape(py5.QUADS):
            tf.no_stroke()
            if idx != 3:
                tf.texture_mode(py5.NORMAL)
                tf.texture(imagem)
            tf.vertices(face)
        tc.add_child(tf)
    return tc


def setup():
    global SLOTS
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.no_smooth()
    py5.frame_rate(1)
    py5.color_mode(py5.HSB, 360, 100, 100)
    background()
    lado = int(LADO * 0.8)
    buffer_lado = (LADO - lado) // 2
    for y0 in range(MARGEM, HEIGHT - MARGEM, LADO):
        y0 += buffer_lado
        y1 = y0 + lado
        for x0 in range(MARGEM, WIDTH - MARGEM, LADO):
            x0 += buffer_lado
            x1 = x0 + lado
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
        with py5.push_matrix():
            py5.translate(0, 0, -400)
            for y0 in range(0, max_y, LADO):
                y1 = y0 + LADO
                for x0 in range(0, max_x, LADO):
                    x1 = x0 + LADO
                    partial = new_frame[y0:y1, x0:x1]
                    py5_img = create_image_from_numpy(partial, "RGBA", dst=py5_img)
                    forma = cria_forma(LADO, py5_img)
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
