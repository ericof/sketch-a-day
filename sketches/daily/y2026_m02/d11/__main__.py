"""2026-02-11
Eye 01
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

inner_radius_i = 40
inner_radius = 90
inner_radius_sa = 320
inner_radius_sb = 198
outer_radius = 550

d = 0.0
e = 0.0
g = 0.0

noise_amp = 20
noise_factor = 33
inner_noise_factor = 10

inner_alpha = 255
outer_alpha = 15

thick = 10
step = 0.8
point_step = 0.9
point_index = 0

stars_pg = None
num_stars = 8
star_objects: list["Star"] = []


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


class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.px = x
        self.py = y
        self.vx = 0.0
        self.vy = 0.0
        self.ang = py5.atan2(y - (py5.height / 2), x - (py5.width / 2))

    def is_active(self):
        return on_screen(self.px, self.py)

    def update(self, acc):
        self.vx += py5.cos(self.ang) * acc
        self.vy += py5.sin(self.ang) * acc

        self.px = self.x
        self.py = self.y

        self.x += self.vx
        self.y += self.vy

    def draw(self):
        speed = py5.sqrt(self.vx * self.vx + self.vy * self.vy)
        alpha = py5.remap(speed, 0, 3, 0, 255)
        alpha = py5.constrain(alpha, 0, 255)

        stars_pg.stroke(255, alpha)
        stars_pg.line(self.x, self.y, self.px, self.py)


def setup():
    global stars_pg

    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(cor_fundo)
    # Stars buffer
    stars_pg = py5.create_graphics(py5.width, py5.height)
    with stars_pg.begin_draw():
        stars_pg.stroke(250)
        stars_pg.stroke_weight(1)

    # Seed stars
    for _ in range(num_stars):
        star_objects.append(Star(py5.random(py5.width), py5.random(py5.height)))

    # Particle system (ring between 75 and 150)
    num_balls = 10_000
    inner_r = 75
    outer_r = 150

    for _ in range(num_balls):
        ang = py5.random(py5.TWO_PI)  # radians
        r = py5.random(inner_r, outer_r)
        x = py5.cos(ang) * r
        y = py5.sin(ang) * r

        # Match original: v = (x,y)*2 ; a = (x,y)*0.018 ; radius = 2.5
        balls.append(Ball(x, y, x * 2.0, y * 2.0, x * 0.018, y * 0.018, 2.5))


def draw_stars():
    global star_objects

    with stars_pg.begin_draw():
        stars_pg.clear()

        acc = py5.remap(py5.mouse_x, 0, py5.width, 0.005, 0.2)

        kept: list[Star] = []
        for s in star_objects:
            s.update(acc)
            s.draw()
            if s.is_active():
                kept.append(s)

        star_objects = kept

        while len(star_objects) < num_stars:
            star_objects.append(Star(py5.random(py5.width), py5.random(py5.height)))

    py5.image(stars_pg, 0, 0)


def draw_rings():
    global d, e, g, point_index

    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro)

        full_turn = py5.TWO_PI

        # --- Inner dotted line ring ---
        if d < full_turn:
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
                    alpha = py5.remap(
                        j, inner_radius_i, outer_radius, inner_alpha, outer_alpha
                    )
                    mix = py5.remap(j, 0, (outer_radius - inner_radius), 0, 1)

                    c3 = py5.color(247, 127, 0)
                    c4 = py5.color(255, 255, 255)
                    ci = lerp_color_rgba(c4, c3, mix)

                    py5.no_stroke()
                    py5.fill(py5.red(ci), py5.green(ci), py5.blue(ci), alpha)
                    y = py5.noise(j / noise_factor / 3, py5.frame_count) * noise_amp
                    py5.circle(j, y, 1)
                    j += point_step

        # --- Middle “muscle” ring ---
        if e < full_turn:
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
                    alpha = py5.remap(
                        i, inner_radius, outer_radius, inner_alpha, outer_alpha
                    )
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

        # --- Outer solid rings (two passes) ---
        if g < full_turn:
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
                    py5.circle(i, 0, 1)

                    point_index += 1
                    i += point_step

            with py5.push_matrix():
                py5.rotate(g)
                start = (
                    inner_radius_sb
                    + 10 * py5.cos(2.5 * py5.frame_count)
                    + py5.noise(py5.frame_count / inner_noise_factor / 1.2) * 40
                    + py5.random(-2, 2)
                )
                i = start
                while i < outer_radius:
                    alpha = py5.remap(
                        i,
                        inner_radius,
                        outer_radius,
                        inner_alpha - 90,
                        outer_alpha - 15,
                    )
                    mix = py5.remap(i, 0, (outer_radius - inner_radius), 0, 1)

                    c7 = py5.color(0, 150, 199)
                    c8 = py5.color(10, 36, 99)
                    ci = lerp_color_rgba(c7, c8, mix)

                    py5.no_stroke()
                    py5.fill(py5.red(ci), py5.green(ci), py5.blue(ci), alpha)
                    py5.circle(i, 0, 1)

                    point_index += 1
                    i += point_step
        else:
            py5.no_loop()
            return

    # Updates (original was degrees; now radians)
    d += py5.radians(step * py5.random(0.5, 2))
    g += py5.radians(step * 0.2)
    e += py5.radians(step * py5.random(0.5, 0.8))
    point_index = 0

    # Particles
    with py5.push():
        py5.translate(py5.width / 2, py5.height / 2)
        for b in balls:
            b.update()
            b.draw()


def draw():
    with py5.push():
        py5.translate(0, 0, -100)
        draw_stars()
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
