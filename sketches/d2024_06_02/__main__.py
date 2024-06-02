"""2024-06-02
Grades sobrepostas 4
Exercício de criação de grades sobrepostas
png
Sketch,py5,CreativeCoding
"""

from dataclasses import dataclass

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


@dataclass
class Celula:
    x: int
    y: int
    pg: py5.Py5Graphics
    largura: int
    altura: int
    fundo: tuple[int, int, int]


GRADES: list[list[Celula]] = []
PASSO: int = 100
QUADRADO: int = 100
DIFF_PASSO_QUADRADO: int = PASSO - QUADRADO
MAX_INTERNO: int = 10
PASSO_INTERNO: float = QUADRADO / MAX_INTERNO


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(0)
    params = [
        (-500 + (i * PASSO / 2), 500 - (i * PASSO / 2), PASSO) for i in range(0, 18)
    ]
    for idx, (pi, pf, passo) in enumerate(params):
        GRADES.append([])
        pi = int(pi)
        pf = int(pf)
        for x in range(pi, pf, passo):
            for y in range(pi, pf, passo):
                pg = py5.create_graphics(QUADRADO, QUADRADO)
                for _ in range(py5.random_int(2, MAX_INTERNO)):
                    h = 5 + (idx * 30)
                    s = 100
                    b = py5.random_int(
                        80 - int(40 / (idx + 1)), 100 - int(40 / (idx + 1))
                    )
                    cor = [h, s, b]
                celula = Celula(x, y, pg, QUADRADO, QUADRADO, cor)
                GRADES[idx].append(celula)


def draw():
    py5.background(0)
    for idx, grade in enumerate(GRADES):
        angulo = py5.radians((idx + 2) * 15)
        with py5.push_matrix():
            py5.translate(py5.width / 2, py5.height / 2)
            py5.rotate(angulo)
            for _, celula in enumerate(grade):
                pg = celula.pg
                pg.begin_draw()
                pg.shape_mode(py5.CENTER)
                pg.background(*celula.fundo)
                pg.end_draw()
                x = celula.x + (DIFF_PASSO_QUADRADO / 2)
                y = celula.y + (DIFF_PASSO_QUADRADO / 2)
                with py5.push_style():
                    pg.fill("#000")
                    pg.stroke("#000")
                    py5.square(x - 4, y - 4, QUADRADO + 8)
                py5.image(pg, x, y)
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
