"""2025-02-14
Valentine's Day (or lack of ideas)
Apenas um monte de corações
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers
from utils.draw import cria_grade_ex

sketch = helpers.info_for_sketch(__file__, __doc__)

CELULA_X = 70
CELULA_Y = 70
FORMA_L = CELULA_X * 0.8
FORMA_A = CELULA_Y * 0.6


def calcula_coracao(
    mult_x: int = 400, mult_y: int = 20, passo: int = 2
) -> list[tuple[float, float]]:
    pontos = []
    for angulo in range(0, 360, passo):
        theta = py5.radians(angulo)
        x = mult_x * py5.sin(theta) ** 3
        y = (
            -(
                13 * py5.cos(theta)
                - 5 * py5.cos(2 * theta)
                - 2 * py5.cos(3 * theta)
                - py5.cos(4 * theta)
            )
            * mult_y
        )
        pontos.append((x, y))
    return pontos


def coracao() -> py5.Py5Shape:
    pontos = calcula_coracao()
    forma = py5.create_shape()
    with forma.begin_closed_shape():
        forma.vertices(pontos)
    return forma


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.shape_mode(py5.CORNER)
    py5.rect_mode(py5.CENTER)
    py5.stroke_weight(4)
    forma = coracao()
    grade = cria_grade_ex(py5.width, py5.height, 50, 50, CELULA_X, CELULA_Y, False)
    grossura = 10
    for idx, xb, idy, yb in grade:
        x = xb + CELULA_X / 2
        y = yb + CELULA_Y / 2
        with py5.push_matrix():
            py5.translate(x, y, -60)
            h = 0
            s = 100 if idx % 2 else 80
            b = (100 if idy % 2 else 80) - grossura
            if idy % 2:
                fundo = py5.color(0, 0, 0)
                preenchimento = py5.color(h, s, b)
                contorno = py5.color(h, s, b - 10)
            else:
                fundo = py5.color(h, s, b)
                preenchimento = py5.color(0, 0, 0)
                contorno = py5.color(h, s, b - 10)
            forma.set_stroke(contorno)
            forma.set_fill(preenchimento)
            py5.fill(fundo)
            py5.rect(0, 0, CELULA_X, CELULA_Y)
            largura = FORMA_L + grossura
            altura = FORMA_A + grossura
            py5.shape(forma, 0, 0, largura, altura)
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
