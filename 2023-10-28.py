"""2023-10-28"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from PIL import Image

import numpy as np
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")


def image_transform(data: np.array, width: int, height: int) -> np.array:
    x_min = width // 2 - WIDTH
    x_max = width // 2 + WIDTH
    y_min = height // 2 - HEIGHT
    y_max = height // 2 + HEIGHT
    # Get only the center part of image
    new_data = []
    for x, rows in enumerate(np.swapaxes(data, 1, 0)):
        new_data.append([])
        for values in rows:
            new_data[x].append(values)
    new_data = np.swapaxes(np.array(new_data), 1, 0)
    return new_data[y_min:y_max, x_min:x_max]


def setup():
    py5.size(WIDTH, HEIGHT)
    path = Path(__name__).parent.resolve() / "resources"
    image = Image.open(path / "20230914_172217.jpg")
    width, height = image.size
    img_array = image_transform(np.array(image), width, height)

    pixelate(img_array)
    write_legend([py5.color(255)], IMG_NAME)


def pixelate(img_array):
    pixel_chunk = 40
    x_limite = int((WIDTH // 2) * 1)
    py5.no_stroke()
    for idx, x in enumerate(range(0, x_limite, pixel_chunk)):
        pixel_size = int(HEIGHT / (idx + 1))
        for y in range(0, HEIGHT, pixel_size):
            if y + pixel_size > HEIGHT:
                pixel_size = HEIGHT - y

            block = img_array[y : y + pixel_size, x : x + pixel_chunk]
            avg_color = np.mean(block, axis=(0, 1))
            py5.fill(avg_color[0], avg_color[1], avg_color[2], 100)
            py5.rect(x, y, pixel_chunk, pixel_size)
    for idx, x in enumerate(range(x_limite, WIDTH)):
        pixel_size = 1
        for y in range(0, HEIGHT, pixel_size):
            if y + pixel_size > HEIGHT:
                pixel_size = HEIGHT - y

            block = img_array[y : y + pixel_size, x : x + pixel_chunk]
            avg_color = np.mean(block, axis=(0, 1))
            py5.fill(avg_color[0], avg_color[1], avg_color[2], 100)
            py5.rect(x, y, pixel_chunk, pixel_size)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
