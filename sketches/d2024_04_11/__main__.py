"""2024-04-11
Labirinto I
Exercício de criação de um labirinto a partir de uma grade
png
Sketch,py5,CreativeCoding,grid
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


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
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(220, 80, 80)
    py5.ellipse_mode(py5.CENTER)
    py5.rect_mode(py5.CENTER)
    margem_x = -20
    margem_y = -30
    largura = 47
    altura = 47
    grade = cria_grade(margem_x, margem_y, largura, altura, False)
    py5.no_fill()
    py5.stroke_weight(4)
    for x, y in grade:
        h = py5.random_int(30, 90)
        s = py5.random_int(60, 70)
        b = py5.random_int(70, 90)
        py5.stroke(h, s, b)
        if py5.random_int(0, 1):
            coordenadas = (x, y, x + largura, y + altura)
        else:
            coordenadas = (x, y + altura, x + largura, y)
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
