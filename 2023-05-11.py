"""2023-05-11"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from opensimplex import OpenSimplex
from pathlib import Path

import math
import numpy as np
import py5
import random


IMG_NAME = Path(__file__).name.replace(".py", "")


# Set up the OpenSimplex noise generator
noise_generator = OpenSimplex(seed=958351)

# Constants
scale = 5
cols = int(WIDTH / scale)
rows = int(HEIGHT / scale)
num_lines = 800
line_length = 40
ll_array = np.arange(line_length)

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
    i = np.array([i * 0.1 for i in np.arange(0, cols)])
    j = np.array([j * 0.2 for j in np.arange(0, rows)])
    angle_field = noise_generator.noise2array(i, j)
    draw_circuit()


def draw_circuit():
    py5.stroke_weight(4)
    for idy, _ in enumerate(range(num_lines)):
        # Choose a random starting point
        x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        # Set the initial color for the line
        hue = random.randint(0, 360)
        py5.stroke(hue, 100, 100, 50)
        py5.circle(x, y, 15)
        direction = 1.01 if idy % 2 else -1.05
        for idx, _ in enumerate(ll_array):
            # Get the grid indices for the current position
            i, j = int(x / scale), int(y / scale)

            # If the current position is outside the grid, break the loop
            if not (0 <= i < cols and 0 <= j < rows):
                break
            # Get the angle for this point
            angle_raw = angle_field[i][j]

            # Convert the noise value to an angle
            angle = py5.radians((map_value(angle_raw, -1, 1, 0, 360) // 45) * 45)
            # Calculate the x and y components of the vector
            x_component = 0
            y_component = 0

            if idx % 2:
                x_component = math.cos(angle) * scale * py5.random_int(1, 10)
            else:
                y_component = math.sin(angle) * scale * py5.random_int(1, 10)

            # Calculate the new position
            x_new, y_new = x + x_component * direction, y + y_component * direction

            # Draw the line segment
            py5.line(x, y, x_new, y_new)

            # Update the position
            x, y = x_new, y_new

        py5.circle(x, y, 15)

    write_legend(["#000000"], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
