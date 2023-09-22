"""2023-09-22"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from PIL import Image
from random import shuffle

import numpy as np
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")


def load_image(name: str):
    folder = Path(__name__).parent.resolve() / "resources"
    path = folder / name
    image = Image.open(path)
    width, height = image.size
    return np.array(image), width, height


def shuffle_columns(img_1_data) -> np.array:
    data, width, height = img_1_data
    x_min = width // 2 - WIDTH
    x_max = width // 2 + WIDTH
    y_min = height // 2 - HEIGHT
    y_max = height // 2 + HEIGHT
    # Get only the center part of image
    new_image = np.swapaxes(data[y_min:y_max, x_min:x_max], 1, 0)
    shuffle(new_image)
    return np.swapaxes(new_image, 1, 0)


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(py5.color(248, 241, 219))
    py5.background(py5.color(0))
    raw_image_1, image_1_w, image_1_y = load_image("20230914_172217.jpg")
    img_1_data = (raw_image_1, image_1_w, image_1_y)
    img_data = shuffle_columns(img_1_data)
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
