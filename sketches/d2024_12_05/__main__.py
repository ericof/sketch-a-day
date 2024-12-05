"""2024-12-05
Grades e Paletas III
Exercício de criação de grade com arcos e uma duas palestas de cores
png
Sketch,py5,CreativeCoding
"""

from collections import deque

import py5

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)


LARGURA = helpers.LARGURA
ALTURA = helpers.ALTURA
MARGEM = -80
CELULA = 80

GRADE = ["#F589A3", "#EF562F"]

PALETA_1 = deque(
    [
        "#2E1B36",
        "#724C8F",
        "#DAC1D6",
        "#CFC41C",
        "#DFDDA5",
        "#2E1B36",
        "#724C8F",
        "#DAC1D6",
    ]
)

PALETA_2 = deque(
    [
        "#E22C2B",
        "#EB7A52",
        "#EECF41",
        "#166E31",
        "#3A51DB",
        "#E22C2B",
        "#EB7A52",
        "#EECF41",
    ]
)


def setup():
    py5.size(LARGURA, ALTURA, py5.P3D)
    py5.background(0)
    py5.rect_mode(py5.CENTER)
    grade = cria_grade(
        int(LARGURA * 1.5), int(ALTURA * 1.5), MARGEM, MARGEM, CELULA, CELULA, False
    )
    opcoes = len(GRADE)
    for idx, (x0, y0) in enumerate(grade):
        if idx % 10 == 0:
            PALETA_1.rotate(py5.random_int(1, 4))
            PALETA_2.rotate(py5.random_int(2, 4))
        idx_alternativo = -1
        if idx_opcao := (idx % opcoes):
            idx_alternativo = 0
        preenchimento = GRADE[idx_opcao]
        traco = GRADE[idx_alternativo]
        py5.fill(preenchimento)
        py5.stroke(traco)
        py5.square(x0, y0, CELULA)
        with py5.push_style():
            py5.no_stroke()
            with py5.push_matrix():
                py5.translate(x0, y0)
                alt = 1 if idx_opcao else -1
                py5.fill(PALETA_1[-2])
                py5.circle(-CELULA // 2, -CELULA // 2, CELULA)
                py5.rotate(py5.HALF_PI * alt)
                py5.fill(PALETA_1[-1])
                py5.arc(0, 0, CELULA, CELULA, 0, py5.PI / 2)
                py5.arc(0, 0, CELULA, CELULA, py5.PI, 3 * py5.PI / 2)
                PALETA_1.rotate()
                py5.fill(PALETA_2[-1])
                py5.arc(0, 0, CELULA, CELULA, py5.PI / 2, py5.PI)
                py5.arc(0, 0, CELULA, CELULA, 3 * py5.PI / 2, py5.TAU)
                PALETA_2.rotate(-1)
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
