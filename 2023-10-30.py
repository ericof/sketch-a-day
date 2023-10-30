"""2023-10-30"""
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
    image = Image.open(path / "torii.jpg")
    img_array = np.array(image)

    pixelate(img_array)
    write_legend([py5.color(0)], IMG_NAME)


def pixelate(img_array):
    x = 0
    pixel_chunks = np.logspace(1.6, 0.1, num=45)
    py5.no_stroke()
    for pixel_chunk in pixel_chunks:
        pixel_chunk = int(pixel_chunk)
        for y in range(0, HEIGHT, pixel_chunk):
            block = img_array[y : y + pixel_chunk, x : x + pixel_chunk]
            avg_color = np.max(block, axis=(0, 1))
            py5.fill(avg_color[0], avg_color[1], avg_color[2], 100)
            py5.rect(x, y, pixel_chunk, pixel_chunk)
        x += pixel_chunk

    for x in range(x, WIDTH):
        pixel_size = 1
        for y in range(0, HEIGHT, pixel_size):
            if y + pixel_size > HEIGHT:
                pixel_size = HEIGHT - y

            block = img_array[y : y + pixel_size, x : x + pixel_chunk]
            colors = block[0][0]
            py5.fill(colors[0], colors[1], colors[2], 100)
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
