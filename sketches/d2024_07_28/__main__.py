"""2024-07-28
Padrões 2
Exercício de criação de padrões circulares dentro de uma grade
png
Sketch,py5,CreativeCoding,abav
"""

from random import choice

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

GRADE = []
QUADRADO = 96

CORES = [
    (0, 0, 0),
]

POS = [
    (QUADRADO, QUADRADO / 2),
    (0, QUADRADO / 2),
    (QUADRADO / 2, 0),
    (QUADRADO / 2, QUADRADO),
]


def setup():
    global PG
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    for idy, y in enumerate(range(100, 700, 100), 1):
        for idx, x in enumerate(range(100, 700, 100), 1):
            pg = py5.create_graphics(QUADRADO, QUADRADO)
            fundo = (240, 233, 211)
            num_circulos = py5.random_int(3, 5)
            circulos = []
            pos = choice(POS)
            for _ in range(num_circulos):
                tamanho = py5.random_int(2, QUADRADO - 20)
                passo = py5.TWO_PI / py5.random_int(2, 22)
                cor = choice(CORES)
                circulos.append((pos, tamanho, cor))
            GRADE.append((pg, (x, y), (idx, idy), fundo, passo, circulos))


def draw():
    py5.background(10, 10, 10)
    f = py5.frame_count
    i = 0
    for pg, (x, y), (idx, idy), fundo, passo, circulos in GRADE:
        pg.begin_draw()
        pg.background(*fundo)
        for circulo in circulos:
            (xc, yc), d, cor = circulo
            s = py5.cos(py5.radians(f * 2) + i * passo)
            d += 65 * s
            pg.no_fill()
            pg.stroke(*cor)
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
