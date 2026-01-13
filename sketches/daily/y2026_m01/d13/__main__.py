"""2026-01-13
Tiles 01
Desenho de uma malha de formas que se transformam ciclicamente.
ericof.com|https://openprocessing.org/sketch/2757066
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)
shapes = []
cor_fundo = py5.color(0)

paleta = gera_paleta("Warhol", True)


def tiling():
    c = 15
    w = py5.width / c

    step_i = py5.cos(py5.PI / 6)
    step_j = py5.cos(py5.PI / 3) * 3

    i = -1.5
    while i < c:
        j = -1
        while j <= c:
            x = i * w + w / 2
            y = j * w + w / 2
            shapes.append(Shape(x, y, w))
            shapes.append(
                Shape(
                    x + (w / 2) * py5.cos(py5.PI / 6),
                    y + (w * 1.5) * py5.cos(py5.PI / 3),
                    w,
                )
            )
            j += step_j
        i += step_i


class Shape:
    def __init__(self, x, y, w):
        self.x = x
        self.y = y
        self.w = w
        self.current_w = w
        self.shape_type = 0

        dst = py5.dist(center_x, center_y, x, y)
        max_dst = py5.sqrt((py5.width / 2) ** 2 + (py5.height / 2) ** 2)
        self.timer = -int(py5.remap(dst, 0, max_dst, 100, 0))

        self.t1 = 30
        self.t2 = self.t1 + 30
        self.t3 = self.t2 + 120

        self.clr = py5.random_choice(paleta)

    def show(self):
        py5.push_matrix()
        py5.translate(self.x, self.y)
        py5.rotate(py5.PI / 6)

        py5.fill(self.clr)
        py5.no_stroke()

        if self.shape_type == 0:
            py5.begin_shape()
            a = 0.0
            step = py5.TAU / 6
            while a < py5.TAU - 1e-9:
                py5.vertex(
                    self.current_w * 0.5 * py5.cos(a), self.current_w * 0.5 * py5.sin(a)
                )
                a += step
            py5.end_shape(py5.CLOSE)

        elif self.shape_type == 1:
            py5.circle(0, 0, self.current_w * 0.5)

        elif self.shape_type == 2:
            py5.rect(0, 0, self.current_w * 0.75, self.current_w * 0.9)

        elif self.shape_type == 3:
            py5.begin_shape()
            a = 0.0
            step = py5.TAU / 3
            while a < py5.TAU - 1e-9:
                py5.vertex(
                    self.current_w * 0.5 * py5.cos(a), self.current_w * 0.5 * py5.sin(a)
                )
                a += step
            py5.end_shape(py5.CLOSE)

        py5.no_stroke()
        py5.fill("#00000050")

        py5.pop_matrix()

    def update(self):
        if 0 < self.timer < self.t1:
            nrm = py5.norm(self.timer, 0, self.t1 - 1)
            self.current_w = py5.lerp(self.w, self.w * 0.2, nrm**3)

        elif self.t1 < self.timer < self.t2:
            nrm = py5.norm(self.timer, self.t1, self.t2 - 1)
            self.current_w = py5.lerp(self.w * 0.2, self.w, nrm ** (1 / 3))

        if self.timer == self.t1:
            self.shape_type += 1
            if self.shape_type == 4:
                self.shape_type = 0
            self.clr = py5.random_choice(paleta)

        if self.timer > self.t3:
            self.timer = 0

        self.timer += 1

    def run(self):
        self.show()
        self.update()


def setup():
    global center_x, center_y
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.background(cor_fundo)
    py5.color_mode(py5.HSB, 360, 100, 100)
    center_x, center_y = helpers.DIMENSOES.centro
    tiling()


def draw():
    py5.background("#020202")
    for s in shapes:
        s.run()
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
