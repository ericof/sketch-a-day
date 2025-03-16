"""2025-03-16
Planejamento 02
A partir de uma grade, colocamos quadrados com pequenas imperfeições
png
Sketch,py5,CreativeCoding
"""

from random import choice, shuffle

import py5

from utils import helpers
from utils.draw import cria_grade_ex, gera_paleta

sketch = helpers.info_for_sketch(__file__, __doc__)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0, 0, 0)
    py5.rect_mode(py5.CORNER)
    paleta = gera_paleta("DJ1")
    shuffle(paleta)
    margem_x = -400
    margem_y = -400
    largura_base = 60
    altura_base = 40
    py5.stroke_weight(2)
    grade = cria_grade_ex(
        py5.width, py5.height, margem_x, margem_y, largura_base, altura_base, False
    )
    for idx, x, idy, y in grade:
        with py5.push_matrix():
            py5.translate(0, 0, py5.random_gaussian(-70, 3))
            py5.stroke("#111")
            cor_interna = choice(paleta)
            py5.fill(cor_interna)
            mult = py5.random(1.2, 1.6)
            largura = largura_base * mult
            altura = altura_base * mult
            forma = py5.create_shape(py5.RECT, 0, 0, largura, altura)
            rotacao_max = py5.random_gaussian(
                (idy // 2) * (-1 if idx < 10 else 1), idx / 30
            )
            forma.rotate(py5.radians(rotacao_max))
            py5.shape(forma, x, y)
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
