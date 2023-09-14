"""2023-09-13"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from PIL import Image

import numpy as np
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")


def load_image(name: str):
    folder = Path(__name__).parent.resolve() / "resources"
    path = folder / name
    image = Image.open(path)
    width, height = image.size
    return np.array(image), width, height


def image_transform(data: np.array, width: int, height: int) -> np.array:
    x_min = width // 2 - WIDTH
    x_max = width // 2 + WIDTH
    y_min = height // 2 - HEIGHT
    y_max = height // 2 + HEIGHT
    # Get only the center part of image
    new_data = []
    for x, rows in enumerate(np.swapaxes(data, 1, 0)):
        if (x // 40) % 2 == 1:
            rows = list(rows[30:]) + list(rows[:30])
        new_data.append([])
        for values in rows:
            new_data[x].append(values)
    new_data = np.swapaxes(np.array(new_data), 1, 0)
    return new_data[y_min:y_max, x_min:x_max]


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(py5.color(248, 241, 219))
    py5.background(py5.color(0))
    raw_image, image_w, image_y = load_image("20230914_172217.jpg")
    img_data = image_transform(raw_image, image_w, image_y)
    py5_img = py5.create_image_from_numpy(img_data, "RGB")
    py5.image(py5_img, 0, 0, WIDTH, HEIGHT)
    write_legend([py5.color(255, 255, 255)], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
