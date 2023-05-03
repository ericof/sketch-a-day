"""2023-05-02"""
from helpers import HEIGHT
from helpers import save_frame
from helpers import save_gif
from helpers import tmp_path
from helpers import WIDTH
from helpers import write_legend
from opensimplex import OpenSimplex
from pathlib import Path

import numpy as np
import py5
import random


IMG_NAME = Path(__file__).name.replace(".py", "")

PATH = tmp_path()

FRAMES = []


# Set up the OpenSimplex noise generator
noise_generator = OpenSimplex(seed=13542)

# Constants
scale = 1
cols = int(WIDTH / scale)
rows = int(HEIGHT / scale)
num_lines = 5000
line_length = 7000

# Initialize the angle field
angle_field = [[0 for _ in range(cols)] for _ in range(rows)]


def settings():
    py5.size(WIDTH, HEIGHT)


def setup():
    global angle_field
    py5.background(py5.color(248, 241, 219))
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100, 100)
    i = np.arange(cols)
    i_noise = i * 0.01
    j = np.arange(rows)
    j_noise = j * 0.01
    noise = noise_generator.noise2array(i_noise, j_noise)
    for i in range(cols):
        for j in range(rows):
            # Convert the noise value to an angle
            angle = py5.remap(noise[i][j], -1, 1, 0, 2 * np.pi)
            angle_field[i][j] = angle


def draw():
    frame = py5.frame_count
    py5.background(0)
    for idy in range(num_lines):
        # Choose a random starting point
        x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)

        # Set the initial color for the line
        hue = random.randint(180, 270)
        py5.stroke(hue, 100, 100, 50)
        direcao = 0 if idy % 2 else 1
        for idx in range(line_length):
            stroke = 3 if idx < 5 else 1
            py5.stroke_weight(stroke)
            # Get the grid indices for the current position
            i, j = int(x / scale), int(y / scale)

            # If the current position is outside the grid, break the loop
            if not (0 <= i < cols and 0 <= j < rows):
                break

            # Get the angle for this point
            angle = angle_field[i][j]

            # Calculate the x and y components of the vector
            x_component = np.cos(angle) * scale * (frame / 10)
            y_component = np.sin(angle) * scale * (frame / 10)

            # Calculate the new position
            if direcao:
                x_new, y_new = x + x_component, y + y_component
            else:
                x_new, y_new = x - x_component, y - y_component

            # Draw the line segment
            py5.line(x, y, x_new, y_new)

            # Update the position
            x, y = x_new, y_new

    write_legend([py5.color(360, 0, 100)], IMG_NAME)
    FRAMES.append(save_frame(PATH, IMG_NAME, frame))
    py5.window_title(f"FR: {py5.get_frame_rate():.1f} | Frame Count: {frame}")


def key_pressed():
    if py5.key == " ":
        py5.no_loop()
        print(f"Saving {len(FRAMES)} frames")
        save_gif(IMG_NAME, FRAMES, loop=None)
        py5.exit_sketch()


py5.run_sketch()
