from helpers import HEIGHT
from helpers import WIDTH
from helpers import save_frame
from helpers import write_legend
from helpers import save_gif
from helpers import tmp_path
from random import shuffle
from pathlib import Path
from py5 import create_image_from_numpy

import numpy as np
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")
PATH = tmp_path()
FRAMES = []

distancia = -8000
x = WIDTH / 2
signal = 1
passo_z = 3
passo_x = 0.15
noise_increment = 0.009


def setup():
    global mesh_x, mesh_y, rgb_map
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.color_mode(py5.HSB, 360, 256, 256)
    cs = [py5.color(py5.random_int(10, 80), 128 + h / 2, 100) for h in range(256)]
    shuffle(cs)
    rgb_map = np.dstack(
        (
            [c >> 16 & 0xF0 for c in cs],
            [c >> 8 & 0xF0 for c in cs],
            [c & 0xF0 for c in cs],
        )
    )
    mesh_x, mesh_y = np.meshgrid(
        np.arange(0, py5.width * noise_increment, noise_increment),
        np.arange(0, py5.height * noise_increment * 2, noise_increment * 3),
    )


def draw():
    global x, distancia, signal, passo_z, passo_x
    py5.background(0)
    py5_img = None
    py5.directional_light(200, 80, 153, -2, 2, -2)
    py5.ambient_light(300, 0, 20)
    py5.no_stroke()
    frame = py5.frame_count
    distancia += signal * (frame * passo_z)
    if distancia > -720:
        passo_z = 1.1
        passo_x = 0.1
    x -= passo_x * frame
    print(frame, x, distancia)
    py5.translate(x, HEIGHT / 2, distancia)
    py5.rotate_y(py5.radians(frame * 1.001))
    h = py5.remap(
        py5.os_noise(mesh_x, mesh_y, frame * noise_increment / 2),
        -1,
        1,
        0,
        255,
    ).astype(np.uint8)
    npa = rgb_map[:, h][0]
    py5_img = create_image_from_numpy(npa, "RGB", dst=py5_img)

    sphere = py5.create_shape(py5.SPHERE, 400)
    sphere.set_texture(py5_img)
    sphere.set_ambient("#FF0000")
    py5.shape(sphere)
    write_legend([py5.color(360, 0, 255)], img_name=IMG_NAME)
    FRAMES.append(save_frame(PATH, IMG_NAME, frame))
    py5.window_title(str(round(py5.get_frame_rate(), 1)))
    if distancia > 1000:
        print("Finished")
        py5.no_loop()


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_gif(IMG_NAME, FRAMES, duration=50)
        py5.exit_sketch()


py5.run_sketch()
