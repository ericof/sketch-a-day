"""2024-04-29
Grades e Círculos
Exercício de preenchimento de uma grade com círculos
png
Sketch,py5,CreativeCoding,grid
"""

import py5

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)

GRADE = None
LARGURA = 60
ALTURA = 60
MARGEM = 100


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA)
    py5.background(0)
    py5.rect_mode(py5.CORNERS)
    py5.ellipse_mode(py5.CENTER)
    py5.color_mode(py5.HSB, 360, 100, 100)
    GRADE = cria_grade(py5.width, py5.height, MARGEM, MARGEM, LARGURA, ALTURA, False)
    meia_largura = LARGURA / 2
    meia_altura = ALTURA / 2
    with py5.push_style():
        x0, y0 = GRADE[0]
        xf, yf = GRADE[-1]
        py5.no_stroke()
        py5.fill(210, 100, 100)
        py5.rect(
            x0 + meia_largura, y0 + meia_altura, xf + meia_largura, yf + meia_altura
        )
    with py5.push_style():
        py5.stroke(360, 50, 100)
        py5.fill(360, 0, 100)
        for xb, yb in GRADE:
            x = xb + meia_largura
            y = yb + meia_altura
            py5.ellipse(x, y, LARGURA, ALTURA)
    helpers.write_legend(sketch=sketch)


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
