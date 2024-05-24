"""2024-05-24
Grades Sobrepostas II
Criação de duas grades, de diferentes tamanhos
png
Sketch,py5,CreativeCoding
"""

from random import choice

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

GRADE = []
GRADE_FUNDO = []
QUADRADO = 60
QUADRADO_FUNDO = 80


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
    (QUADRADO / 2, QUADRADO / 3),
    (QUADRADO, QUADRADO),
    (QUADRADO, 0),
]


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    grades = [
        [-490, 500, 100, (120, 117, 106), GRADE_FUNDO, QUADRADO_FUNDO],
        [-190, 200, 80, (240, 233, 211), GRADE, QUADRADO],
    ]
    for inicio, final, passo_grade, fundo, grade, t_quadrado in grades:
        for idy, y in enumerate(range(inicio, final, passo_grade), 1):
            for idx, x in enumerate(range(inicio, final, passo_grade), 1):
                pg = py5.create_graphics(t_quadrado, t_quadrado)
                num_circulos = py5.random_int(2, 3)
                circulos = []
                for _ in range(num_circulos):
                    pos = choice(POS)
                    tamanho = py5.random_int(5, 50)
                    passo = py5.TWO_PI / py5.random_int(2, 22)
                    cor = choice(CORES)
                    circulos.append((pos, tamanho, cor))
                grade.append(
                    (pg, (x, y), (idx, idy), fundo, passo, circulos, t_quadrado)
                )


def draw():
    py5.background(248, 241, 219)
    f = py5.frame_count
    i = 0
    with py5.push_matrix():
        py5.translate(py5.width / 2, py5.height / 2)
        for rot, grade in [(0, GRADE_FUNDO), (45, GRADE)]:
            py5.rotate(py5.radians(rot))
            for pg, (x, y), (idx, idy), fundo, passo, circulos, t_quadrado in grade:
                pg.begin_draw()
                pg.background(*fundo)
                for circulo in circulos:
                    (xc, yc), d, cor = circulo
                    s = py5.cos(py5.radians(f * 2) + i * passo)
                    d += 50 * s
                    pg.fill(*cor)
                    pg.circle(xc, yc, d)
                pg.end_draw()
                with py5.push_style():
                    py5.stroke("#000")
                    py5.stroke_weight(3)
                    py5.square(x - 1, y - 1, t_quadrado + 2)
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
