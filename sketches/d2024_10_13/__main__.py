"""2024-10-13
Mosaico 01
Exercício de criação de um mosaico em uma grade.
png
Sketch,py5,CreativeCoding
"""

from random import choice, shuffle

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

PALETA = [
    "#032035",
    "#120D2D",
    "#1C8EAF",
    "#425AC6",
    "#7EC0E0",
    "#CAC9D1",
    "#D0341E",
    "#F7D744",
    "#F87109",
    "#FDAA08",
]


def cria_grade(
    margem_x: int, margem_y: int, celula_x: int, celula_y: int, alternada: bool = True
):
    """Cria uma grade."""
    pontos = []
    celula_x = int(celula_x)
    celula_y = int(celula_y)
    yi = margem_y
    yf = py5.height - margem_y
    for idy, y in enumerate(range(yi, yf, celula_y)):
        if (y + celula_y) > yf:
            break
        buffer = int(celula_x / 2) if (alternada and idy % 2) else 0
        xi = margem_x - buffer
        xf = py5.width - margem_x
        for x in range(xi, xf, celula_x):
            pontos.append((x, y))
    return pontos


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(248, 241, 219)
    py5.rect_mode(py5.CORNER)
    shuffle(PALETA)
    margem_x = -15
    margem_y = -25
    largura = 30
    altura = 30
    py5.stroke_weight(2)
    grade = cria_grade(margem_x, margem_y, largura, altura, True)
    for x, y in grade:
        cor_traco = choice(PALETA)
        py5.stroke(cor_traco)
        cor_interna = choice(PALETA)
        py5.fill(cor_interna)
        py5.rect(x, y, largura, altura)
    with py5.push_matrix():
        py5.translate(0, 0, 10)
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
