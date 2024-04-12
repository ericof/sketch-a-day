"""2024-04-12
Labirinto II
Exercício de criação de um labirinto a partir de uma grade
png
Sketch,py5,CreativeCoding,grid
"""

import py5

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)

GRADE = None
LARGURA = 47
ALTURA = 47


def setup():
    global GRADE
    py5.size(helpers.LARGURA, helpers.ALTURA)
    py5.frame_rate(1)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.ellipse_mode(py5.CENTER)
    py5.rect_mode(py5.CENTER)
    margem_x = -20
    margem_y = -30
    GRADE = cria_grade(
        py5.width, py5.height, margem_x, margem_y, LARGURA, ALTURA, False
    )
    py5.no_fill()


def draw():
    py5.background(220, 80, 80)
    py5.stroke_weight(6)
    for x, y in GRADE:
        h = py5.random_int(30, 90)
        s = py5.random_int(60, 70)
        b = py5.random_int(70, 90)
        py5.stroke(h, s, b)
        direcao = py5.random_int(5)
        terco_largura = LARGURA / 3
        terco_altura = ALTURA / 3
        if direcao == 0:
            coordenadas = (x, y, x + LARGURA, y + ALTURA)
        elif direcao == 1:
            coordenadas = (x, y + ALTURA, x + LARGURA, y)
        elif direcao == 2:
            coordenadas = (x + terco_largura, y, x + terco_largura, y + ALTURA)
        elif direcao == 3:
            coordenadas = (x, y + terco_altura, x + LARGURA, y + terco_altura)
        elif direcao == 4:
            coordenadas = (x + 2 * terco_largura, y, x + 2 * terco_largura, y + ALTURA)
        elif direcao == 5:
            coordenadas = (x, y + 2 * terco_altura, x + LARGURA, y + 2 * terco_altura)
        py5.line(*coordenadas)
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
