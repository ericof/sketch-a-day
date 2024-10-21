"""2024-10-22
Mais mosaícos 02
A partir de uma grade, colocamos quadrados com pequenas imperfeições
png
Sketch,py5,CreativeCoding
"""

from random import choice, shuffle

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

PALETA = [
    "#7c00fe",
    "#f9e400",
    "#ffaf00",
    "#f5004f",
]


def cria_grade(
    xi: int,
    xf: int,
    yi: int,
    yf: int,
    celula_x: int,
    celula_y: int,
    alternada: bool = True,
):
    """Cria uma grade."""
    pontos = []
    celula_x = int(celula_x)
    celula_y = int(celula_y)
    for idy, y in enumerate(range(yi, yf + 1, celula_y)):
        if (y + celula_y) > yf:
            break
        buffer = int(celula_x / 2) if (alternada and idy % 2) else 0
        for x in range(xi - buffer, xf + 1, celula_x):
            pontos.append((x, y))
    return pontos


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(248, 241, 219)
    py5.rect_mode(py5.CORNER)
    shuffle(PALETA)
    margem_x = -200
    margem_y = -200
    largura_base = 42
    altura_base = 42
    grade = cria_grade(
        margem_x,
        py5.width - margem_x,
        margem_y,
        py5.height - margem_y,
        largura_base,
        altura_base,
        True,
    )
    # shuffle(grade)
    for x, y in grade:
        py5.stroke_weight(py5.random(0, 3))
        py5.stroke("#000")
        cor_interna = choice(PALETA)
        py5.fill(cor_interna)
        mult_l = py5.random(1.03, 1.3)
        mult_a = py5.random(1.03, 1.3)
        largura = largura_base * mult_l
        altura = altura_base * mult_a
        forma = py5.create_shape(py5.RECT, 0, 0, largura, altura)
        rotacao_max = py5.remap(y, -200, 1000, 0, 6) + py5.remap(x, -200, 1000, 0, 6)
        forma.rotate(py5.radians(py5.random(-rotacao_max, rotacao_max)))
        py5.shape(forma, x, y)
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
