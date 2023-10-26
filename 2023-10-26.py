"""2023-10-26"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import numpy as np
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")


def setup():
    py5.size(WIDTH, HEIGHT)
    path = Path(__name__).parent.resolve() / "resources"
    img = py5.load_image(path / "20230914_172217.jpg")
    w = img.width
    h = img.height
    py5.image(img, -w // 2, -h // 2)  # Display the original image

    pixelate()
    write_legend([py5.color(255)], IMG_NAME)


def pixelate():
    py5.load_np_pixels()
    img_array = py5.np_pixels
    pixel_chunk = 10
    x_limite = int((WIDTH // 4) * 3)
    for x in range(0, x_limite, pixel_chunk):
        pixel_size = int(WIDTH // (x / pixel_chunk + 1))

        for y in range(0, HEIGHT, pixel_size):
            if y + pixel_size > HEIGHT:
                pixel_size = HEIGHT - y

            block = img_array[y : y + pixel_size, x : x + pixel_chunk]
            avg_color = np.mean(block, axis=(0, 1))

            py5.fill(avg_color[0], avg_color[1], avg_color[2], avg_color[3])
            py5.no_stroke()
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
