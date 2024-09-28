"""2024-09-28
Mondrian Redux 05
Releitura 2D de Piet Mondrian
png
Sketch,py5,CreativeCoding
"""

import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

PALETA = [
    "#F7D744",
    "#D0341E",
    "#D0341E",
    "#120D2D",
    "#425AC6",
    "#CAC9D1",
]


class Circle:
    """A little class representing an SVG circle."""

    def __init__(self, cx, cy, r, color=None):
        """Initialize the circle with its centre, (cx,cy) and radius, r.

        icolor is the index of the circle's color.

        """
        self.cx, self.cy, self.r = cx, cy, r
        self.color = color

    def overlap_with(self, cx, cy, r):
        """Does the circle overlap with another of radius r at (cx, cy)?"""
        d = np.hypot(cx - self.cx, cy - self.cy)
        return d < r + self.r


class Circles:
    """A class for drawing circles-inside-a-circle."""

    def __init__(
        self,
        width=800,
        height=800,
        R=400,
        n=800,
        rho_min=0.005,
        rho_max=0.05,
        colors=None,
    ):
        """Initialize the Circles object.

        width, height are the SVG canvas dimensions
        R is the radius of the large circle within which the small circles are
        to fit.
        n is the maximum number of circles to pack inside the large circle.
        rho_min is rmin/R, giving the minimum packing circle radius.
        rho_max is rmax/R, giving the maximum packing circle radius.
        colors is a list of SVG fill color specifiers to be referenced by
            the class identifiers c<i>. If None, a default palette is set.

        """

        self.width, self.height = width, height
        self.R, self.n = R, n
        # The centre of the canvas
        self.CX, self.CY = self.width // 2, self.height // 2
        self.rmin, self.rmax = R * rho_min, R * rho_max
        self.colors = colors or ["#993300", "#a5c916", "#00AA66", "#FF9900"]

    def _place_circle(self, r):
        # The guard number: if we don't place a circle within this number
        # of trials, we give up.
        guard = 500
        while guard:
            # Pick a random position, uniformly on the larger circle's interior
            cr, cphi = (
                self.R * np.sqrt(np.random.random()),
                2 * np.pi * np.random.random(),
            )
            cx, cy = cr * np.cos(cphi), cr * np.sin(cphi)
            if cr + r < self.R:
                # The circle fits inside the larger circle.
                if not any(
                    circle.overlap_with(self.CX + cx, self.CY + cy, r)
                    for circle in self.circles
                ):
                    # The circle doesn't overlap any other circle: place it.
                    circle = Circle(
                        cx + self.CX,
                        cy + self.CY,
                        r,
                        color=self.colors[np.random.randint(len(self.colors))],
                    )
                    self.circles.append(circle)
                    return
            guard -= 1

    def __call__(self) -> list[Circle]:
        """Place the little circles inside the big one."""

        # First choose a set of n random radii and sort them. We use
        # random.random() * random.random() to favour small circles.
        self.circles = []
        r = self.rmin + (self.rmax - self.rmin) * np.random.random(
            self.n
        ) * np.random.random(self.n)
        r[::-1].sort()
        # Do our best to place the circles, larger ones first.
        for i in range(self.n):
            self._place_circle(r[i])
        return self.circles


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    circles = Circles(width=800, height=800, R=400, n=2000, colors=PALETA)
    for circle in circles():
        x = circle.cx
        y = circle.cy
        r = circle.r
        color = circle.color
        with py5.push_style():
            py5.stroke(color)
            py5.fill(color)
            py5.circle(x, y, r)
    helpers.write_legend(sketch=sketch)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    helpers.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
