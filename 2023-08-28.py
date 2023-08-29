"""2023-08-28"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from helpers.circles import Circle as BaseCircle
from helpers.circles import Circles
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

FUNDO = (360, 0, 100)


class Circle(BaseCircle):
    def _fill(self):
        return FUNDO

    def _stroke(self):
        x = self.cx
        y = self.cy
        s = abs(WIDTH / 2 - x) / 4
        b = abs(HEIGHT / 2 - y) / 4
        h = (s + b) * 1.8
        return (h, s, b)

    def draw(self):
        """Draw the circle."""
        diameter = self.r * 2
        s = py5.create_shape(py5.ELLIPSE, 0, 0, diameter, diameter)
        s.set_fill(py5.color(*self.fill))
        s.set_stroke(py5.color(*self.stroke))
        s.set_stroke_weight(self.stroke_weight)
        py5.shape(s, self.cx, self.cy)


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(py5.color(*FUNDO))
    r = WIDTH
    n = 10000
    fill = FUNDO
    reverse_fill = FUNDO
    stroke = (100, 100, 100)
    stroke_weight = 0
    circle = Circles(
        cx=WIDTH / 2,
        cy=HEIGHT / 2,
        r=r,
        n=n,
        rho_min=0.005,
        rho_max=0.20,
        fill=fill,
        reverse_fill=reverse_fill,
        stroke=stroke,
        stroke_weight=stroke_weight,
        circles_r_limit=5,
        guard=400,
        debug=True,
    )
    # Initial circle
    circle_0 = Circle(
        cx=WIDTH / 2,
        cy=HEIGHT / 2,
        r=200,
        fill=(255, 0, 0),
        stroke=stroke,
        stroke_weight=8,
    )
    circle.circles.append(circle_0)
    # Populate other circles
    circle.populate()
    circle.draw()
    write_legend([py5.color(0)], img_name=IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
