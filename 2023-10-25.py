"""2023-10-25"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from PIL import Image

import numpy as np
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")


def setup():
    py5.size(WIDTH, HEIGHT)
    path = Path(__name__).parent.resolve() / "resources"
    img = py5.load_image(path / "20230914_172217.jpg")
    py5.image(img, 0, 0)  # Display the original image

    pixelate_half_x(img)


def pixelate_half_x(img):
    py5.load_np_pixels()
    img_array = py5.np_pixels
    pixel_chunk = 5

    for x in range(0, WIDTH // 2, pixel_chunk):
        pixel_size = int(WIDTH // (x / pixel_chunk + 1))

        for y in range(0, HEIGHT, pixel_size):
            if y + pixel_size > HEIGHT:
                pixel_size = HEIGHT - y

            block = img_array[y : y + pixel_size, x : x + pixel_chunk]
            avg_color = np.mean(block, axis=(0, 1))

            py5.fill(avg_color[0], avg_color[1], avg_color[2])
            py5.no_stroke()
            py5.rect(x, y, pixel_chunk, pixel_size)
    write_legend([py5.color(255)], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
