"""2023-10-29"""
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
    pixel_chunk = 5
    x_limite = int((WIDTH // 3) * 2)
    passo = pixel_chunk // (x_limite / pixel_chunk)
    py5.no_stroke()
    for idx, x in enumerate(range(0, x_limite, pixel_chunk)):
        pixel_size = pixel_chunk - (idx * passo)
        pixel_size = int(pixel_size if pixel_size else 1)
        for y in range(0, HEIGHT, pixel_size):
            if y + pixel_size > HEIGHT:
                pixel_size = HEIGHT - y

            block = img_array[y : y + pixel_size, x : x + pixel_chunk]
            avg_color = np.median(block, axis=(0, 1))
            py5.fill(avg_color[0], avg_color[1], avg_color[2], 100)
            py5.rect(x, y, pixel_chunk, pixel_size)

    for idx, x in enumerate(range(x_limite, WIDTH)):
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
