"""2024-05-13
Grade e círculos 6
Inspirado por um sketch to Alexandre Villares
gif
Sketch,py5,CreativeCoding,abav
"""

from random import choice

import py5
import py5_tools

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

GRADE = []
QUADRADO = 96

CORES = [
    (0, 0, 0),
    (127, 143, 110),
    (179, 176, 133),
    (200, 200, 200),
    (212, 198, 170),
    (218, 211, 189),
    (90, 119, 168),
    (187, 137, 30),
    (30, 30, 30),
    (40, 50, 60),
]

POS = [
    (0, 0),
    (0, QUADRADO),
    (QUADRADO / 2, QUADRADO / 2),
    (QUADRADO / 2, 0),
    (0, QUADRADO / 2),
    (QUADRADO / 2, QUADRADO),
    (QUADRADO, QUADRADO / 2),
    (QUADRADO, QUADRADO),
    (QUADRADO, 0),
]


def setup():
    global PG
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    for idy, y in enumerate(range(100, 700, 100), 1):
        for idx, x in enumerate(range(100, 700, 100), 1):
            pg = py5.create_graphics(QUADRADO, QUADRADO)
            fundo = (52 + idx, 140, 89 + idy)
            num_circulos = py5.random_int(3, 5)
            circulos = []
            for _ in range(num_circulos):
                pos = choice(POS)
                tamanho = py5.random_int(2, 80)
                passo = py5.TWO_PI / py5.random_int(2, 40)
                cor = choice(CORES)
                circulos.append((pos, tamanho, cor))
            GRADE.append((pg, (x, y), (idx, idy), fundo, passo, circulos))


def draw():
    py5.background(52, 140, 89)
    f = py5.frame_count
    i = 0
    for pg, (x, y), (idx, idy), fundo, passo, circulos in GRADE:
        pg.begin_draw()
        pg.background(*fundo)
        for circulo in circulos:
            (xc, yc), d, cor = circulo
            s = py5.sin(py5.radians(f * 2) + i * passo)
            d += 80 * s
            pg.fill(*cor)
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
    py5.exit_sketch()


if __name__ == "__main__":
    py5_tools.animated_gif(
        f"{sketch.path}/{sketch.day}.gif",
        count=30,
        period=0.2,
        duration=0.01,
        block=False,
    )
    py5.run_sketch()
