"""2024-04-23
Circuíto IX
Exercício de criação de um circuíto a partir de uma grade
png
Sketch,py5,CreativeCoding,grid
"""

import py5

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)

GRADE = None
LARGURA = 70
ALTURA = 43


def setup():
    global GRADE
    py5.size(helpers.LARGURA, helpers.ALTURA)
    py5.frame_rate(1)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.ellipse_mode(py5.CENTER)
    py5.rect_mode(py5.CENTER)
    margem_x = -90
    margem_y = -67
    GRADE = cria_grade(
        py5.width, py5.height, margem_x, margem_y, LARGURA, ALTURA, False
    )
    py5.no_fill()


def draw():
    py5.background(230, 100, 50)
    py5.stroke_weight(3)
    for x, y in GRADE:
        h = py5.random_int(39, 40)
        s = py5.random_int(94, 95)
        b = py5.random_int(60, 80)
        py5.stroke(h, s, b)
        direcao = py5.random_int(1)
        if direcao == 0:
            coordenadas = (x, y, x + LARGURA, y + ALTURA)
        elif direcao == 1:
            coordenadas = (x, y + ALTURA, x + LARGURA, y)
        py5.line(*coordenadas)
        with py5.push_style():
            py5.stroke_weight(1)
            py5.fill(h, s, b)
            py5.square(coordenadas[0], coordenadas[1], LARGURA / 4)
    helpers.write_legend(sketch=sketch, cor="#FFF", frame="#000")


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
