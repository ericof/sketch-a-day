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


def load_images(pattern="2023-*.png") -> list:
    folder = Path(__name__).parent.resolve() / "images"
    image_data = {}
    for path in folder.glob(pattern):
        data = np.array(Image.open(path))
        image_data[path.name] = data
    days = sorted([k for k in image_data.keys()])
    image_list = []
    for day in days:
        image_list.append(image_data[day])
    return image_list


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(py5.color(248, 241, 219))
    py5.background(py5.color(0))
    image_list = load_images("2023-09-*.png")
    img_array = np.array(image_list)
    mean_image = np.mean(img_array, axis=0).astype(np.uint8)
    max_image = np.max(img_array, axis=0).astype(np.uint8)
    med_image = np.median(img_array, axis=0).astype(np.uint8)
    std_image = np.std(img_array, axis=0).astype(np.uint8)
    py5_img_01 = py5.create_image_from_numpy(mean_image, "RGB")
    py5_img_02 = py5.create_image_from_numpy(max_image, "RGB")
    py5_img_03 = py5.create_image_from_numpy(med_image, "RGB")
    py5_img_04 = py5.create_image_from_numpy(std_image, "RGB")
    w = WIDTH // 2
    h = HEIGHT // 2
    py5.image(py5_img_01, 0, 0, w, h)
    py5.image(py5_img_02, w, 0, w, h)
    py5.image(py5_img_03, 0, h, w, h)
    py5.image(py5_img_04, w, h, w, h)
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
