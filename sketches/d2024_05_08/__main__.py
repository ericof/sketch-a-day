"""2024-05-08
Grade e círculos
Inspirado por um sketch to Alexandre Villares
png
Sketch,py5,CreativeCoding,abav
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

PG = None
QUADRADO = 98


def setup():
    global pg
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    pg = py5.create_graphics(QUADRADO, QUADRADO)
    py5.frame_rate(3)


def draw():
    py5.background(46, 11, 97)
    f = py5.frame_count
    step = py5.TWO_PI / 16
    i = 0
    for idy, y in enumerate(range(100, 700, 100), 1):
        for idx, x in enumerate(range(100, 700, 100), 1):
            pos = (idy * 10) + idx
            sem = f * pos
            s = py5.cos(py5.radians(sem * 2) + i * step)
            d = py5.random_int(10, 50) + (50 * s)
            xc = py5.remap(f % 50, 0, 50, 0, QUADRADO)
            yc = py5.remap(s, -1, 1, 0, QUADRADO)
            pg.begin_draw()
            pg.background(100, 200, 0)
            h = (pos * f) * s % 360
            s = 60
            b = 70
            pg.fill(h, s, b)
            print(f, sem, s, yc, h, s, b)
            pg.circle(xc, yc, d)
            pg.end_draw()
            py5.image(pg, x, y)
            i += 1
    helpers.write_legend(sketch=sketch, frame="#000")


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
