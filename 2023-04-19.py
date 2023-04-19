"""2023-04-19"""
from helpers import HEIGHT
from helpers import save_frame
from helpers import save_gif
from helpers import tmp_path
from helpers import WIDTH
from pathlib import Path

import py5
import random

IMG_NAME = Path(__file__).name.replace(".py", "")

PATH = tmp_path()

FRAMES = []

FONTS = ["Courier", "Verdana", "Futura", "Arial", "Impact"]

FONT_LIMITS = (8, 24)

SPEED_LIMITS = (4, 12)


class NumberDrop:
    def __init__(self, number, x, size=12):
        self.lateral_speed = (1 / random.randint(2, 6)) * random.randint(-1, 1)
        font_family = random.choice(FONTS)
        self.number = number
        self.base_x = x
        self.x = x
        self.font = py5.create_font(font_family, size)
        self.y = random.randint(-360, -60)
        self.speed = random.randint(*SPEED_LIMITS)
        self.should_accumulate = True

    def fall(self):
        if self.y < py5.height:
            self.y += self.speed
            self.x += self.lateral_speed
        if self.y > py5.height and not self.should_accumulate:
            self.x = self.base_x
            self.y = random.randint(-400, -100)
            self.speed = random.randint(*SPEED_LIMITS)


drops = []


def setup():
    py5.size(800, 800)
    global drops
    num_drops = py5.width // 4
    for i in range(num_drops):
        for _ in range(3):
            x_seed = random.randint(-20, 20)
            drops.append(
                NumberDrop(
                    f"{random.randint(0, 9)}",
                    random.randint(-10, 800) + x_seed,
                    random.randint(*FONT_LIMITS),
                )
            )


def background():
    py5.background(17, 27, 64, 180)
    py5.fill(60, 60, 60)
    py5.text_font(py5.create_font("Space Mono", 20))
    for x0 in range(5, py5.width, 17):
        for y in range(5, py5.height, 15):
            char = "."
            x = x0 if y % 2 else x0 - 5
            py5.text(char, x, y)
            py5.text(char, x + 1, y + 1)


def draw():
    frame_count = py5.frame_count
    background()
    for drop in drops:
        py5.text_font(drop.font)
        # Ghost trace
        base_green = 200
        for i in range(4):
            green = base_green + (i * 20)
            py5.fill(255, green, 255)
            py5.text(drop.number, drop.x, drop.y - (3 - i))
        drop.fall()
    # Save only a third of the frames
    if frame_count % 2:
        FRAMES.append(save_frame(PATH, IMG_NAME, frame_count))
        py5.window_title(f"FR: {py5.get_frame_rate():.1f} | Frame Count: {frame_count}")


def key_pressed():
    if py5.key == " ":
        py5.no_loop()
        print(f"Saving {len(FRAMES)} frames")
        save_gif(IMG_NAME, FRAMES, loop=1)
        py5.exit_sketch()


py5.run_sketch()
