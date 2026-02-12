"""2026-02-12
Eye 02
Desenho que se assemelha a um olho
ericof.com|https://openprocessing.org/sketch/1307209
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

balls: list["Ball"] = []

inner_radius_i = 50
inner_radius = 90
inner_radius_sa = 160
inner_radius_sb = 350
outer_radius = 500

d = 0.0
e = 0.0
g = 0.0

noise_amp = 40
noise_factor = 33
inner_noise_factor = 20

inner_alpha = 100
outer_alpha = 15

thick = 2
step = 0.8
point_step = 0.75
point_index = 0


def lerp_color_rgba(c1, c2, t):
    t = py5.constrain(t, 0, 1)
    r = py5.lerp(py5.red(c1), py5.red(c2), t)
    g_ = py5.lerp(py5.green(c1), py5.green(c2), t)
    b = py5.lerp(py5.blue(c1), py5.blue(c2), t)
    a = py5.lerp(py5.alpha(c1), py5.alpha(c2), t)
    return py5.color(r, g_, b, a)


def on_screen(x, y):
    return 0 <= x <= py5.width and 0 <= y <= py5.height


class Ball:
    def __init__(self, px, py, vx, vy, ax, ay, r):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.r = r

    def update(self):
        # Integrate
        self.vx += self.ax
        self.vy += self.ay
        self.px += self.vx
        self.py += self.vy

        # Flow field-ish noise steering (same spirit as original)
        noise_fx = 35
        noise_fy = 35

        nx = py5.noise(self.px / noise_fx, self.py / noise_fy, 10)
        ny = py5.noise(self.px / noise_fx, self.py / noise_fy, 100)

        self.vx = py5.remap(nx, 0, 1, -1, 1) * 2.5
        self.vy = py5.remap(ny, 0, 1, -1, 1) * 2.5

    def draw(self):
        dist_ = py5.sqrt(self.px * self.px + self.py * self.py)
        alpha = py5.remap(dist_, inner_radius, outer_radius, 100, 0)
        alpha = py5.constrain(alpha, 0, 255)

        py5.no_stroke()
        py5.fill(255, 255, 255, alpha)
        py5.circle(self.px, self.py, self.r)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.background(cor_fundo)

    num_balls = 5_000
    inner_r = 50
    outer_r = 400

    for _ in range(num_balls):
        ang = py5.random(py5.TWO_PI)  # radians
        r = py5.random(inner_r, outer_r)
        x = py5.cos(ang) * r
        y = py5.sin(ang) * r

        balls.append(Ball(x, y, x * 2.0, y * 2.0, x * 0.018, y * 0.018, 3.5))


def inner_ring(d: float, radius: int = 1):
    with py5.push_matrix():
        py5.rotate(d)
        start = (
            inner_radius_i
            + py5.noise(
                py5.sin(py5.frame_count / inner_noise_factor / 10),
                py5.cos(py5.frame_count / inner_noise_factor / 10),
            )
            * 15
            + py5.random(-3, 3)
        )
        j = start
        while j < outer_radius:
            alpha = py5.remap(j, inner_radius_i, outer_radius, inner_alpha, outer_alpha)
            mix = py5.remap(j, 0, (outer_radius - inner_radius), 0, 1)

            c3 = py5.color(247, 127, 0)
            c4 = py5.color(255, 255, 255)
            ci = lerp_color_rgba(c4, c3, mix)

            py5.no_stroke()
            py5.fill(py5.red(ci), py5.green(ci), py5.blue(ci), alpha)
            y = py5.noise(j / noise_factor / 3, py5.frame_count) * noise_amp
            py5.circle(j, y, radius)
            j += point_step


def middle_ring(e: float, point_index: int):
    with py5.push_matrix():
        py5.rotate(e)

        start = (
            inner_radius
            + 10 * py5.sin(20 * py5.frame_count)
            + py5.noise(py5.frame_count / inner_noise_factor) * 50
            + py5.random(-5, 5)
        )
        i = start
        while i < outer_radius:
            alpha = py5.remap(i, inner_radius, outer_radius, inner_alpha, outer_alpha)
            mix = py5.remap(i, 0, (outer_radius - inner_radius), 0, 1)

            c1 = py5.color(0, 167, 225)
            c2 = py5.color(255, 255, 255)
            ci = lerp_color_rgba(c2, c1, mix)

            thick1 = (
                py5.noise(py5.frame_count * 10) * thick
                + 20 * (py5.sin(10 * py5.frame_count) + 1)
                + py5.random(-5, 5)
            )
            iris_stroke = 1.6 if point_index < thick1 else 1.0

            py5.no_stroke()
            py5.fill(py5.red(ci), py5.green(ci), py5.blue(ci), alpha)
            y = py5.noise(i / noise_factor, py5.frame_count) * noise_amp
            py5.circle(i, y, iris_stroke)

            point_index += 1
            i += point_step


def outer_ring(g: float, point_index: int, radius: int = 1):
    with py5.push_matrix():
        py5.rotate(g)
        start = (
            inner_radius_sa
            + 10 * py5.sin(2.5 * py5.frame_count)
            + py5.noise(py5.frame_count / inner_noise_factor / 1.1) * 40
            + py5.random(-2, 2)
        )
        i = start
        while i < outer_radius:
            alpha = py5.remap(
                i, inner_radius, outer_radius, inner_alpha, outer_alpha - 15
            )
            mix = py5.remap(i, 0, (outer_radius - inner_radius), 0, 1)

            c5 = py5.color(3, 71, 72)
            c6 = py5.color(20, 129, 186)
            ci = lerp_color_rgba(c6, c5, mix)

            py5.no_stroke()
            py5.fill(py5.red(ci), py5.green(ci), py5.blue(ci), alpha)
            py5.circle(i, 0, radius)

            point_index += 1
            i += point_step


def draw_rings():
    global d, e, g, point_index

    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, 10)

        full_turn = py5.TWO_PI

        # --- Inner dotted line ring ---
        if d < full_turn:
            inner_ring(d, 1)

        # --- Middle “muscle” ring ---
        if e < full_turn:
            middle_ring(e, point_index)

        # --- Outer solid rings (two passes) ---
        if g < full_turn:
            outer_ring(g, point_index, 1)

        else:
            save_and_close()

    d += py5.radians(step * py5.random(0.5, 2))
    g += py5.radians(step * 0.2)
    e += py5.radians(step * py5.random(0.5, 0.8))
    point_index = 0

    # Particles
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro)
        for b in balls:
            b.update()
            b.draw()


def draw():
    with py5.push():
        py5.translate(0, 0, -100)
        draw_rings()
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
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
