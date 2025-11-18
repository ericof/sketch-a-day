"""2025-11-18
Distributing circles 04
Exercício de distribuição de círculos dentro de um círculo maior.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)


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
        colors: deque[py5.Py5Color],
        width=800,
        height=800,
        R=400,
        n=800,
        rho_min=0.005,
        rho_max=0.05,
        guard=1000,
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
        self.guard = guard
        self.colors = colors
        self.img = np.ones((height, width))

    def _circle_fits(self, icx, icy, r):
        """If I fits, I sits."""

        if icx - r < 0 or icy - r < 0:
            return False
        if icx + r >= self.width or icy + r >= self.height:
            return False

        return all((
            self.img[icx - r, icy],
            self.img[icx + r, icy],
            self.img[icx, icy - r],
            self.img[icx, icy + r],
        ))

    def apply_circle_mask(self, icx, icy, r):
        """Zero all elements of self.img in circle at (icx, icy), radius r."""

        x, y = np.ogrid[0 : self.width, 0 : self.height]
        r2 = (r + 1) ** 2
        mask = (x - icx) ** 2 + (y - icy) ** 2 <= r2
        self.img[mask] = 0

    def _place_circle(self, r, c_idx=None):
        """Attempt to place a circle of radius r within the image figure.

        c_idx is a list of indexes into the self.colors list, from which
        the circle's colour will be chosen. If None, use all colors.

        """

        if not c_idx:
            c_idx = range(len(self.colors))

        # Get the coordinates of all non-zero image pixels
        img_coords = np.nonzero(self.img)
        if not img_coords:
            return False

        # The guard number: if we don't place a circle within this number
        # of trials, we give up.
        guard = self.guard
        # For this method, r must be an integer. Ensure that it's at least 1.
        r = max(1, int(r))
        while guard:
            # Pick a random candidate pixel...
            i = np.random.randint(len(img_coords[0]))
            icx, icy = img_coords[0][i], img_coords[1][i]
            # ... and see if the circle fits there
            if self._circle_fits(icx, icy, r):
                self.apply_circle_mask(icx, icy, r)
                circle = Circle(icx, icy, r, color=self.colors[np.random.choice(c_idx)])
                self.circles.append(circle)
                return True
            guard -= 1
        return False

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
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color("#000")
    py5.background(cor_fundo)
    camadas = [
        (-10, gera_paleta("laranja-02", True), 500, 500),
        (-8, gera_paleta("mondrian", True), 800, 400),
        (-6, gera_paleta("pastel", True), 1000, 300),
        (-4, gera_paleta("Colerful", True), 2000, 300),
    ]
    for z, paleta, total, raio in camadas:
        with py5.push():
            py5.translate(*helpers.DIMENSOES.pos_interno, z)
            circles = Circles(
                colors=paleta,
                width=800,
                height=800,
                R=raio,
                n=total,
                guard=1100,
                rho_min=0.0005,
                rho_max=0.20,
            )
            for circle in circles():
                x = circle.cx
                y = circle.cy
                r = circle.r
                color = circle.color
                with py5.push():
                    peso = py5.random_int(1, 3)
                    py5.stroke("#000")
                    py5.stroke_weight(peso)
                    py5.fill(color)
                    py5.circle(x, y, r)

    # Credits and go
    canvas.sketch_frame(
        sketch, cor_fundo, "large_transparent_white", "transparent_white"
    )


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
