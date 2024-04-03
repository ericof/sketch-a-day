"""2024-04-03
Mosaico
Exercício de criação de um mosaico em uma grade.
png
Sketch,py5,CreativeCoding,grid
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


CORES = [
    (127, 143, 110),
    (200, 12, 90),
    (12, 200, 84),
    (179, 176, 133),
    (200, 200, 200),
    (212, 198, 170),
    (218, 211, 189),
    (90, 119, 168),
    (187, 137, 30),
    (30, 30, 30),
    (40, 50, 60),
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
    py5.size(helpers.LARGURA, helpers.ALTURA)
    py5.background(248, 241, 219)
    py5.rect_mode(py5.CORNER)
    margem_x = -5
    margem_y = -5
    largura = 7
    altura = 11
    grade = cria_grade(margem_x, margem_y, largura, altura, False)
    for x, y in grade:
        py5.fill(*py5.random_choice(CORES))
        py5.rect(x, y, largura, altura)
    helpers.write_legend(sketch=sketch, cor="#000")


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
