"""2023-05-02"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from opensimplex import OpenSimplex
from pathlib import Path

import math
import py5
import random


IMG_NAME = Path(__file__).name.replace(".py", "")


# Set up the OpenSimplex noise generator
noise_generator = OpenSimplex(seed=3268)
noise_generator = OpenSimplex(seed=1975)

# Constants
WIDTH = 800
HEIGHT = 800
scale = 5
cols = int(WIDTH / scale)
rows = int(HEIGHT / scale)
num_lines = 5000
line_length = 500

# Initialize the angle field
angle_field = [[0 for _ in range(cols)] for _ in range(rows)]


def map_value(value, start1, stop1, start2, stop2):
    proportion = (value - start1) / (stop1 - start1)
    return start2 + proportion * (stop2 - start2)


def settings():
    py5.size(WIDTH, HEIGHT)


def setup():
    global angle_field
    py5.background(py5.color(248, 241, 219))
    py5.color_mode(py5.HSB, 360, 100, 100, 100)

    for i in range(cols):
        for j in range(rows):
            # Get the noise value for this point
            noise_val = noise_generator.noise2(i * 0.1, j * 0.1)
            # Convert the noise value to an angle
            angle = map_value(noise_val, -1, 1, 0, 2 * math.pi)
            angle_field[i][j] = angle


def draw():
    frame = py5.frame_count
    for _ in range(num_lines):
        # Choose a random starting point
        x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)

        # Set the initial color for the line
        hue = random.randint(0, 360)
        py5.stroke(hue, 100, 100, 50)
        for idx in range(line_length):
            stroke = 2 if idx < 5 else 1
            py5.stroke_weight(stroke)
            # Get the grid indices for the current position
            i, j = int(x / scale), int(y / scale)

            # If the current position is outside the grid, break the loop
            if not (0 <= i < cols and 0 <= j < rows):
                break

            # Get the angle for this point
            angle = angle_field[i][j]

            # Calculate the x and y components of the vector
            x_component = math.cos(angle) * scale * (frame / 10)
            y_component = math.sin(angle) * scale * (frame / 10)

            # Calculate the new position
            x_new, y_new = x + x_component, y + y_component

            # Draw the line segment
            py5.line(x, y, x_new, y_new)

            # Update the position
            x, y = x_new, y_new

    write_legend(["#000000"], IMG_NAME)
    if frame > 8:
        py5.no_loop()
    else:
        py5.window_title(f"FR: {py5.get_frame_rate():.1f} | Frame Count: {frame}")


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
