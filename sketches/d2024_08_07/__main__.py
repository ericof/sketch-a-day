"""2024-08-07
Padrões 12
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

POS = [
    (QUADRADO, 0),
    (0, QUADRADO),
    (QUADRADO, QUADRADO),
    (0, 0),
]
POS_R = [
    (0, QUADRADO),
    (QUADRADO, 0),
    (0, 0),
    (QUADRADO, QUADRADO),
]


def setup():
    global PG
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    for idy, y in enumerate(range(-300, 300, 80), 1):
        for idx, x in enumerate(range(-300, 300, 80), 1):
            canal = (idy + idx) % 3
            pg = py5.create_graphics(QUADRADO, QUADRADO)
            fundo = (240, 233, 211)
            if canal == 1:
                fundo = (250, 233, 80)
            elif canal == 2:
                fundo = (120, 116, 105)
            num_circulos = py5.random_int(10, 20)
            circulos = []
            pos = choice(POS)
            pos_r = POS_R[POS.index(pos)]
            passo = 200 // num_circulos
            for idc in range(num_circulos):
                valor = (passo * idc) + 55
                cor = [0, 0, 0]
                cor[canal] = valor
                tamanho = py5.random_int(2, QUADRADO)
                passo = py5.TWO_PI / py5.random_int(2, 22)
                circulos.append((pos, tamanho, cor))
                circulos.append((pos_r, tamanho, cor))
            GRADE.append((pg, (x, y), (idx, idy), fundo, passo, circulos))


def draw():
    py5.background(10, 10, 10)
    f = py5.frame_count
    i = 0
    with py5.push_matrix():
        py5.translate(py5.width / 2, py5.height / 2)
        angulo = 0
        for pg, (x, y), (idx, idy), fundo, passo, circulos in GRADE:
            py5.rotate(py5.radians(angulo))
            pg.begin_draw()
            pg.background(*fundo)
            for circulo in circulos:
                (xc, yc), d, cor = circulo
                s = py5.cos(py5.radians(f * 2) + i * passo)
                d += 65 * s
                pg.no_fill()
                pg.stroke(*cor)
                pg.stroke_weight(QUADRADO / abs(d))
                pg.circle(xc, yc, d)
            pg.end_draw()
            py5.image(pg, x, y)
            i += 1
            angulo += py5.random(0.1, 5.0)
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
