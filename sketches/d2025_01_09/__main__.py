"""2025-01-09
Public transport seating
Padrão de tecido utilizado pelo hipotético metrô da Asa Norte de Brasília
png
Sketch,py5,CreativeCoding,genuary,genuary2025,genuary9
"""

import py5

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)


FUNDO = "#001A6E"
PALETA = [
    "#074799",
    "#009990",
    "#E1FFBB",
]


def desenha_elemento(xb, yb, largura, altura):
    xc = xb + largura // 2
    yc = yb + altura // 2
    with py5.push_matrix():
        py5.translate(xc, yc, -40)
        py5.rotate_z(145)
        for x in range(-largura + 4, largura - 4):
            y0 = -altura + py5.random_gaussian(4)
            yf = altura + py5.random_gaussian(4)
            py5.stroke_weight(2)
            py5.stroke(py5.random_choice(PALETA))
            py5.line(x, y0, x, yf)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(FUNDO)
    py5.rect_mode(py5.CENTER)
    grade = cria_grade(py5.width, py5.height, 0, 0, 40, 40, True)
    for x, y in grade:
        desenha_elemento(x, y, 40, 40)
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
