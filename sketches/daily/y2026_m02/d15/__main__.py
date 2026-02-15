"""2026-02-15
Eye 05
Desenho que se assemelha a um olho alienígena
ericof.com|https://openprocessing.org/sketch/1307209
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers
from typing import cast

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

balls: list["Ball"] = []

status = True

inner_radius_i = 50
inner_radius = 60
inner_radius_sa = 160
outer_radius = 600

num_balls = 12_000
inner_r = inner_radius
outer_r = 600

d = 0.0
e = 0.0
g = 0.0

noise_amp = 40
noise_factor = 80
inner_noise_factor = 40

inner_alpha = 100
outer_alpha = 80

thick = 2
step = 0.8
point_step = 0.8
point_index = 0

PG_DIMENSAO = 2000, 1000
PG_MEIO = 1000, 500

PG: py5.Py5Graphics | None = None

luz_x = 300
luz_y = 410
luz_z = -1800


def lerp_color_rgba(c1, c2, t):
    t = py5.constrain(t, 0, 1)
    r = py5.lerp(py5.red(c1), py5.red(c2), t)
    g_ = py5.lerp(py5.green(c1), py5.green(c2), t)
    b = py5.lerp(py5.blue(c1), py5.blue(c2), t)
    a = py5.lerp(py5.alpha(c1), py5.alpha(c2), t)
    return py5.color(r, g_, b, a)


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

    def draw(self, pg: py5.Py5Graphics):
        dist_ = py5.sqrt(self.px * self.px + self.py * self.py)
        alpha = py5.remap(dist_, inner_radius, outer_radius, 100, 0)
        alpha = py5.constrain(alpha, 0, 255)
        with pg.push():
            pg.translate(*PG_MEIO)
            pg.no_stroke()
            pg.fill(20, 100, 255, alpha)
            pg.circle(self.px, self.py, self.r)


def center_ring(pg: py5.Py5Graphics, rotation: float, frame: int, radius: int = 1):
    with pg.push():
        pg.translate(*PG_MEIO, -20)
        pg.rotate(rotation)
        j = 0
        while j < inner_radius_sa:
            alpha = py5.remap(j, 0, inner_radius_sa, inner_alpha, 20)
            pg.no_stroke()
            pg.fill(py5.color(0, 0, 0, alpha))
            y = py5.noise(j / noise_factor / 3, frame) * noise_amp
            pg.circle(j, y, radius)
            j += point_step


def inner_ring(pg: py5.Py5Graphics, d: float, frame: int, radius: int = 1):
    seed = frame / inner_noise_factor / 10
    with pg.push():
        pg.translate(*PG_MEIO)
        pg.rotate(d)
        start = (
            inner_radius_i
            + py5.noise(py5.sin(seed), py5.cos(seed)) * 15
            + py5.random(-3, 3)
        )
        j = start
        while j < outer_radius:
            alpha = py5.remap(j, inner_radius_i, outer_radius, inner_alpha, outer_alpha)
            mix = py5.remap(j, 0, (outer_radius - inner_radius), 0, 1)

            c3 = py5.color(247, 127, 0)
            c4 = py5.color(255, 255, 255)
            ci = lerp_color_rgba(c4, c3, mix)

            pg.no_stroke()
            pg.fill(py5.red(ci), py5.green(ci), py5.blue(ci), alpha)
            y = py5.noise(j / noise_factor / 3, py5.frame_count) * noise_amp
            pg.circle(j, y, radius)
            j += point_step


def middle_ring(pg: py5.Py5Graphics, e: float, frame: int, point_index: int):
    frame = py5.frame_count
    with pg.push():
        pg.translate(*PG_MEIO)
        pg.rotate(e)

        start = (
            inner_radius
            + 10 * py5.sin(20 * frame)
            + py5.noise(frame / inner_noise_factor) * 50
            + py5.random(-5, 5)
        )
        i = start
        while i < outer_radius:
            alpha = py5.remap(i, inner_radius, outer_radius, inner_alpha, outer_alpha)
            mix = py5.remap(i, 0, (outer_radius - inner_radius), 0, 1)

            c1 = py5.color(0, 255, 167)
            c2 = py5.color(255, 255, 255)
            ci = lerp_color_rgba(c2, c1, mix)

            thick1 = (
                py5.noise(frame * 10) * thick
                + 20 * (py5.sin(10 * frame) + 1)
                + py5.random(-5, 5)
            )
            iris_stroke = 1.6 if point_index < thick1 else 1.0

            pg.no_stroke()
            pg.fill(py5.red(ci), py5.green(ci), py5.blue(ci), alpha)
            y = py5.noise(i / noise_factor, frame) * noise_amp
            pg.circle(i, y, iris_stroke)

            point_index += 1
            i += point_step


def outer_ring(
    pg: py5.Py5Graphics, g: float, frame: int, point_index: int, radius: int = 1
):
    frame = py5.frame_count
    with pg.push():
        pg.translate(*PG_MEIO)
        pg.rotate(g)
        start = cast(
            float,
            (
                inner_radius_sa
                - 10 * py5.sin(2.5 * frame)
                - py5.noise(frame / inner_noise_factor / 1.1) * 40
                - py5.random(-3, 3)
            ),
        )
        i = start
        while i < outer_radius:
            alpha = py5.remap(
                i, inner_radius, outer_radius, inner_alpha, outer_alpha - 15
            )
            mix = py5.remap(i, 0, (outer_radius - inner_radius), 0, 1)

            c5 = py5.color(3, 72, 65)
            c6 = py5.color(20, 186, 129)
            ci = lerp_color_rgba(c6, c5, mix)

            pg.no_stroke()
            pg.fill(py5.red(ci), py5.green(ci), py5.blue(ci), alpha)
            pg.circle(i, 0, radius)

            point_index += 1
            i += point_step


def draw_rings(pg: py5.Py5Graphics) -> tuple[py5.Py5Graphics, bool]:
    global d, e, g, point_index
    frame = py5.frame_count

    with pg.begin_draw():
        full_turn = py5.TWO_PI

        if d < full_turn:
            center_ring(pg, d, frame, 6)
            inner_ring(pg, d, frame, 1)

        if e < full_turn:
            middle_ring(pg, e, frame, point_index)

        if g < full_turn:
            percentual = (g / full_turn) * 100
            print(f"{percentual:02f}")
            outer_ring(pg, g, frame, point_index, 1)
            for b in balls:
                b.update()
                b.draw(pg)

        d += py5.radians(step * py5.random(0.5, 2))
        e += py5.radians(step * py5.random(0.5, 0.8))
        g += py5.radians(step * py5.random(0.1, 0.3))
        point_index = 0

    return pg, bool(g < full_turn)


def setup():
    global PG
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.background(cor_fundo)
    py5.image_mode(py5.CENTER)

    PG = py5.create_graphics(*PG_DIMENSAO, py5.P3D)
    with PG.begin_draw():
        PG.background(py5.color(255, 255, 255))

    for _ in range(num_balls):
        ang = py5.random(py5.TWO_PI)  # radians
        r = py5.random(inner_r, outer_r)
        x = py5.cos(ang) * r
        y = py5.sin(ang) * r

        balls.append(Ball(x, y, x * 1.45, y * 1.45, x * 0.018, y * 0.018, 3.5))


def draw():
    global PG, status

    if PG:
        pg, status = draw_rings(PG)

    centro = helpers.DIMENSOES.centro
    esfera = py5.create_shape(py5.SPHERE, outer_r / 2)
    with py5.push():
        py5.translate(*centro, -outer_r / 3)
        py5.directional_light(200, 200, 200, luz_x, luz_y, luz_z)
        esfera.set_texture(pg)
        esfera.set_texture_mode(py5.IMAGE)
        esfera.set_stroke(False)
        esfera.rotate_y(py5.radians(90))
        py5.shape(esfera)
    py5.window_title(f"{luz_x} - {luz_y} - {luz_z}")

    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )
    if not status:
        save_and_close()


def key_pressed():
    global luz_x, luz_y, luz_z
    key = py5.key
    match key:
        case "a":
            luz_x -= 10
        case "d":
            luz_x += 10
        case "w":
            luz_y -= 10
        case "s":
            luz_y += 10
        case "r":
            luz_z -= 10
        case "f":
            luz_z += 10
        case " ":
            save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
