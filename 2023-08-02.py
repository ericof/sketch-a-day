"""2023-08-02"""
from helpers import HEIGHT
from helpers import save_frame
from helpers import save_gif
from helpers import tmp_path
from helpers import WIDTH
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")
PATH = tmp_path()
FRAMES = []

FUNDO = py5.color(0)


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)


def draw():
    py5.background(0)
    frame = py5.frame_count
    py5.translate(WIDTH / 2, HEIGHT / 2, -200)
    py5.rotate_x(py5.radians(frame))
    py5.rotate_y(py5.radians(frame))
    base = [
        (-100, 100, 0),
        (-141, 0, 0),
        (-100, -100, 0),
        (0, -141, 0),
        (100, -100, 0),
        (141, 0, 0),
        (100, 100, 0),
        (0, 141, 0),
    ]
    # top vertice
    top = (0, 0, 400)
    # bottom vertice
    bottom = (0, 0, -200)
    # color
    py5.fill(0, 51, 102)
    py5.ambient_light(102, 102, 102)
    py5.light_specular(204, 204, 204)
    py5.directional_light(102, 102, 102, 0, 0, -1)
    py5.shininess(6.0)
    # draw base
    with py5.begin_shape():
        for x, y, z in base:
            py5.vertex(x, y, z)

    # draw sides
    for i in range(len(base)):
        with py5.begin_shape():
            x, y, z = base[i]
            py5.vertex(x, y, z)
            x, y, z = base[(i + 1) % len(base)]
            py5.vertex(x, y, z)
            x, y, z = top
            py5.vertex(x, y, z)
            x, y, z = base[i]
            py5.vertex(x, y, z)
            x, y, z = base[(i + 1) % len(base)]
            py5.vertex(x, y, z)
            x, y, z = bottom
            py5.vertex(x, y, z)

    FRAMES.append(save_frame(PATH, IMG_NAME, frame))
    if frame >= 361:
        save_and_close()
    py5.window_title(f"FR: {py5.get_frame_rate():.1f} | Frame Count: {frame}")


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_gif(IMG_NAME, FRAMES, duration=0.5)
    py5.exit_sketch()


py5.run_sketch()
