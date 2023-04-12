from pathlib import Path

import py5


WIDTH = 800
HEIGHT = 800


def write_legend(palette = None, img_name = ""):
    if palette:
        color = palette[-1]
    else:
        color = "#000"
    py5.fill(color)
    py5.text_size(12)
    py5.text_align(py5.RIGHT)
    py5.text(img_name, WIDTH - 20, HEIGHT - 20)


def save_image(img_name):
    folder = Path(__file__).parent.resolve()
    img_folder = folder / 'Images'
    img_path = img_folder / f"{img_name}.jpg"
    img = py5.get(0, 0, WIDTH, HEIGHT)
    img.save(img_path)
