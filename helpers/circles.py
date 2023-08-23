import py5
import numpy as np


def _random():
    return np.random.random()


def _overlap_with(x0, y0, r0, x1, y1, r1):
    d = np.hypot(x0 - x1, y0 - y1)
    return d < r0 + r1


class Circle:
    """Represent a Circle in py5."""

    cx: float
    cy: float
    r: float
    fill: tuple
    stroke: tuple
    stroke_weight: int = 1

    def __init__(self, cx, cy, r, fill, stroke, stroke_weight: int = 1):
        """Initialize the circle with its centre, (cx,cy) and radius, r."""
        self.cx = cx
        self.cy = cy
        self.r = r
        self.fill = fill
        self.stroke = stroke
        self.stroke_weight = stroke_weight

    def overlap_with(self, cx, cy, r):
        """Does the circle overlap with another of radius r at (cx, cy)?"""
        return _overlap_with(cx, cy, r, self.cx, self.cy, self.r)

    def draw(self):
        """Draw the circle."""
        diameter = self.r * 2
        s = py5.create_shape(py5.ELLIPSE, 0, 0, diameter, diameter)
        s.set_fill(py5.color(*self.fill))
        s.set_stroke(py5.color(*self.stroke))
        s.set_stroke_weight(self.stroke_weight)
        py5.shape(s, self.cx, self.cy)


class Circles:
    """A class for drawing circles-inside-a-circle."""

    def __init__(
        self,
        r=250,
        n=800,
        rho_min=0.005,
        rho_max=0.10,
        cx=400,
        cy=400,
        guard=1500,
        fill=(255, 255, 255),
        reverse_fill=(0, 0, 0),
        stroke=(255, 255, 255),
        stroke_weight=1,
        debug=False,
    ):
        """Initialize the Circles object.
        r is the radius of the large circle within which the small circles are
        to fit.
        n is the maximum number of circles to pack inside the large circle.
        rho_min is rmin/r, giving the minimum packing circle radius.
        rho_max is rmax/r, giving the maximum packing circle radius.
        guard is the number of attempts to place a circle before giving up
        fill is the color fill
        reverse_fill is the color used in children objects
        stroke is the color used on borders
        """
        self.circles = []
        self.r = r
        self.n = n
        self.cx = cx
        self.cy = cy
        self.rmin = r * rho_min
        self.rmax = r * rho_max
        self.guard = guard
        self.fill = fill
        self.reverse_fill = reverse_fill
        self.stroke = stroke
        self.stroke_weight = stroke_weight
        self.debug = debug
        self._circle = Circle(
            self.cx,
            self.cy,
            r,
            fill=self.fill,
            stroke=self.stroke,
            stroke_weight=self.stroke_weight,
        )

    def overlap_with(self, cx, cy, r):
        """Does the circle overlap with another of radius r at (cx, cy)?"""
        return _overlap_with(cx, cy, r, self.cx, self.cy, self.r)

    def draw(self):
        circle = self._circle
        circle.draw()
        self._draw_children()

    def _draw_children(self):
        """Create the image as an SVG file with name filename."""
        for circle in self.circles:
            circle.draw()

    def _place_circle(self, r):
        """Attempt to place a circle of radius r within the larger circle."""
        # The guard number: if we don't place a circle within this number
        # of trials, we give up.
        guard = self.guard
        while guard:
            # Pick a random position, uniformly on the larger circle's interior
            cr = self.r * np.sqrt(_random())
            cphi = 2 * np.pi * _random()
            cx = cr * np.cos(cphi)
            cy = cr * np.sin(cphi)
            if cr + r < self.r:
                # The circle fits inside the larger circle.
                if not any(
                    circle.overlap_with(self.cx + cx, self.cy + cy, r)
                    for circle in self.circles
                ):
                    # The circle doesn't overlap any other circle: place it.
                    x = cx + self.cx
                    y = cy + self.cy
                    fill = self.reverse_fill
                    reverse_fill = self.fill
                    stroke = self.stroke
                    if r < 10:
                        circle = Circle(
                            x,
                            y,
                            r,
                            fill=reverse_fill,
                            stroke=stroke,
                            stroke_weight=1,
                        )
                    else:
                        n = int(r * py5.random_int(8, 10))
                        stroke_weight = self.stroke_weight
                        if r < 50:
                            stroke_weight = 1
                        elif r < 100:
                            stroke_weight = 2
                        elif r < 200:
                            stroke_weight = 3
                        circle = Circles(
                            cx=x,
                            cy=y,
                            r=r,
                            n=n,
                            fill=fill,
                            reverse_fill=reverse_fill,
                            stroke=stroke,
                            stroke_weight=stroke_weight,
                            debug=self.debug,
                        )
                        circle.populate()
                    self.circles.append(circle)
                    return True
            guard -= 1
        return False

    def populate(self):
        """Place the little circles inside the big one.

        c_idx is a list of colour indexes (into the self.colours list) from
        which to select random colours for the circles. If None, use all
        the colours in self.colours.

        """

        # First choose a set of n random radii and sort them. We use
        # random.random() * random.random() to favour small circles.
        r = self.rmin + (self.rmax - self.rmin) * np.random.random(
            self.n
        ) * np.random.random(self.n)
        r[::-1].sort()
        # Do our best to place the circles, larger ones first.
        nplaced = 0
        for i in range(self.n):
            if self._place_circle(r[i]):
                nplaced += 1
        if self.debug:
            print(
                f"{self.cx}, {self.cy}, {self.r}, {nplaced}/{self.n}, {self.fill}, {self.stroke}, {self.fill}"
            )
