"""2025-01-02
Layers upon layers upon layers
Camadas de grades
png
Sketch,py5,CreativeCoding,genuary,genuary2
"""

from random import shuffle

import py5

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)

GRADE_TAMANHO = 310
ALTURA = 30
LARGURA = 30


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(20, 20, 20)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CORNER)
    py5.blend_mode(py5.BLEND)
    grades = []
    for idx, margem in enumerate(range(50, 651, 50)):
        pontos = cria_grade(
            GRADE_TAMANHO + margem * 2,
            GRADE_TAMANHO + margem * 2,
            margem,
            margem,
            LARGURA,
            ALTURA,
            False,
        )
        pontos1 = [(py5.width - x, y) for x, y in pontos]
        pontos2 = [
            (x, py5.height - y)
            for x, y in cria_grade(
                GRADE_TAMANHO + margem * 2,
                GRADE_TAMANHO + margem * 2,
                margem,
                margem,
                LARGURA * py5.random(0.5, 1.2),
                ALTURA * py5.random(0.5, 1.2),
                True,
            )
        ]
        hi = idx * 6.5 + 40
        h = hi + 20
        s = 60 + (idx * 2)
        bi = 100 - (idx * 8)
        b = bi + 20
        grades.append((pontos, py5.color(hi, s, b), py5.color(h, s, bi)))
        grades.append((pontos1, py5.color(h, s, bi), py5.color(hi, s, b)))
        grades.append((pontos2, py5.color(hi, s, bi), py5.color(hi, s - 10, bi)))
    shuffle(grades)
    for idx, (pontos, traco, preenchimento) in enumerate(grades, 1):
        with py5.push_matrix():
            py5.translate(py5.width // 2, py5.height // 2, -(idx * 8))
            py5.rotate_x(-12)
            py5.translate(-py5.width // 2, -py5.height // 1.4, 0)
            for x, y in pontos:
                py5.stroke(traco)
                py5.stroke_weight(2)
                py5.fill(preenchimento)
                py5.rect(x, y, LARGURA, ALTURA)
    py5.stroke("#000")
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
