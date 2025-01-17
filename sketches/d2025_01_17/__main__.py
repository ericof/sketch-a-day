"""2025-01-17
PI = 4
Criando arcos considerando PI = 4
png
Sketch,py5,CreativeCoding,genuary,genuary2025,genuary15
"""

import py5

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)

PI = 4
MEIO_PI = PI / 2

PALETA = [
    "#F7D744",
    "#D0341E",
    "#D0341E",
    "#120D2D",
    "#425AC6",
    "#CAC9D1",
]

PASSO = 80
RAZAO = 2


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(248, 241, 219)
    tamanho = PASSO / RAZAO
    grade = cria_grade(
        py5.width * 2,
        py5.height * 2,
        -py5.width // 2,
        -py5.height // 2,
        PASSO,
        PASSO,
        True,
    )
    with py5.push_style():
        py5.no_fill()
        py5.stroke_cap(py5.ROUND)
        py5.stroke_weight(8)
        for x, y in grade:
            py5.stroke(py5.random_choice(PALETA))
            py5.arc(
                x,
                y + tamanho,
                tamanho,
                tamanho,
                PI,
                3 * MEIO_PI,
            )
            py5.stroke(py5.random_choice(PALETA))
            py5.arc(
                x,
                y,
                tamanho,
                tamanho,
                0,
                MEIO_PI,
            )
            py5.stroke(py5.random_choice(PALETA))
            py5.arc(
                x + (tamanho),
                y,
                tamanho,
                tamanho,
                PI,
                3 * MEIO_PI,
            )
    helpers.write_legend(sketch=sketch, frame="#000", cor="#FFF")


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
