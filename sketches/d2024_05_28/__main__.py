"""2024-05-28
Grade pastel 3
Exercício de animação de grade com formas geométricas concêntricas
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
    numero: int
    forma: py5.RECT | py5.ELLIPSE
    forma_mult: tuple[float, float]
    base: tuple[int, int]


GRADE: list[Celula] = []
PASSO: int = 100
QUADRADO: int = 80
DIFF_PASSO_QUADRADO: int = PASSO - QUADRADO
MAX_INTERNO: int = 10
PASSO_INTERNO: float = QUADRADO / MAX_INTERNO


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    formas = [py5.RECT, py5.ELLIPSE]
    pontos_base = [QUADRADO / 4, QUADRADO / 3, QUADRADO / 2]
    for x in range(100, 700, PASSO):
        for y in range(100, 700, PASSO):
            pg = py5.create_graphics(QUADRADO, QUADRADO)
            base = (py5.random_choice(pontos_base), py5.random_choice(pontos_base))
            forma = py5.random_choice(formas)
            forma_mult = [py5.random_int(60, 80) / 100, py5.random_int(60, 130) / 100]
            celula = Celula(
                x,
                y,
                pg,
                QUADRADO,
                QUADRADO,
                py5.random_int(2, MAX_INTERNO),
                forma,
                forma_mult,
                base,
            )
            GRADE.append(celula)


def draw():
    py5.background(0)
    f = py5.frame_count
    for idx, celula in enumerate(GRADE):
        pg = celula.pg
        pg.begin_draw()
        pg.shape_mode(py5.CENTER)
        pg.background(228, 221, 199)
        pg.no_fill()
        pg.stroke("#000")
        pg.stroke_weight(2)
        for idx in range(celula.numero + 1):
            tamanho = idx * PASSO_INTERNO
            mult_x = py5.cos(py5.radians(f * 2) + idx * 2)
            mult_y = py5.sin(py5.radians(f * 2) + idx * 2)
            tamanho_x = tamanho * celula.forma_mult[0] * mult_x
            tamanho_y = tamanho * celula.forma_mult[1] * mult_y
            xb, yb = celula.base
            forma = pg.create_shape(
                celula.forma, xb, yb, xb + tamanho_x, yb + tamanho_y
            )
            forma.rotate_x(py5.radians(f * 15))
            pg.shape(forma, xb, yb)
        pg.end_draw()
        x = celula.x + (DIFF_PASSO_QUADRADO / 2)
        y = celula.y + (DIFF_PASSO_QUADRADO / 2)
        with py5.push_style():
            pg.fill(188, 181, 119)
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
