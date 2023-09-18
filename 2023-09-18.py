"""2023-09-18"""
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


def merge_images(img_1_data, img_2_data) -> np.array:
    items = []
    for data, width, height in (img_1_data, img_2_data):
        x_min = width // 2 - WIDTH
        x_max = width // 2 + WIDTH
        y_min = height // 2 - HEIGHT
        y_max = height // 2 + HEIGHT
        # Get only the center part of image
        items.append(data[y_min:y_max, x_min:x_max])
    items = np.array(items)
    return np.average(items, axis=0, weights=[5, 5])


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(py5.color(248, 241, 219))
    py5.background(py5.color(0))
    raw_image_1, image_1_w, image_1_y = load_image("20230914_172217.jpg")
    img_1_data = (raw_image_1, image_1_w, image_1_y)
    raw_image_2, image_2_w, image_2_y = load_image("20230914_133628.jpg")
    img_2_data = (raw_image_2, image_2_w, image_2_y)
    img_data = merge_images(img_1_data, img_2_data)
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
