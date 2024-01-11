"""2024-01-11
Genuary 11 - In the style of Anni Albers
Textura composta por vários retângulos listrados.
png
Sketch,py5,CreativeCoding,genuary,genuary11
"""
from random import choice, shuffle

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


CORES = [
    (0, 0, 0),
    (127, 143, 110),
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


def gera_forma(largura, altura, passos, cor_1, cor_2):
    forma = py5.create_shape(py5.GROUP)
    altura_ = altura / passos
    for i in range(0, passos):
        cor = cor_1 if i % 2 else cor_2
        y = i * altura_
        bloco = py5.create_shape(py5.RECT, 0, y, largura, altura_)
        bloco.set_stroke(False)
        bloco.set_fill(py5.color(*cor))
        bloco.set_name(f"Linha_{i:02d}")
        forma.add_child(bloco)
    return forma


def prepara_formas(total, largura, altura, passos):
    formas = []
    for i in range(total):
        cor_1, cor_2 = choice(CORES), choice(CORES)
        forma = gera_forma(largura, altura, passos, cor_1, cor_2)
        forma.set_name(f"Bloco_{i:02d}")
        formas.append(forma)
    return formas


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P2D)
    py5.background(248, 241, 219)
    py5.shape_mode(py5.CORNER)
    margem_x = 40
    margem_y = 50
    largura = 80
    altura = 220
    grade = cria_grade(margem_x, margem_y, largura, altura, False)
    formas = prepara_formas(len(grade), largura, altura, 12)
    shuffle(formas)
    for x, y in grade:
        forma = formas.pop()
        py5.shape(forma, x, y, largura, altura)
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
