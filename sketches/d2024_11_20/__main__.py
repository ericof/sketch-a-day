"""2024-11-20
Circuíto Redux IV
Exercício de criação de um circuíto a partir de uma grade
png
Sketch,py5,CreativeCoding,grid
"""

import py5

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)

GRADE = None
LARGURA = 20
ALTURA = 20
MARGEM_X = 150
MARGEM_Y = 150


def setup():
    global GRADE
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.frame_rate(1)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.ellipse_mode(py5.CENTER)
    py5.rect_mode(py5.CENTER)
    GRADE = cria_grade(
        py5.width, py5.height, MARGEM_X, MARGEM_Y, LARGURA, ALTURA, False
    )
    py5.no_fill()


def draw():
    py5.background("#000")
    py5.stroke_weight(3)
    meio_x = py5.width // 2
    meio_y = py5.height // 2
    with py5.push_matrix():
        py5.translate(meio_x, meio_y)
        for angulo in range(0, 90, 15):
            py5.translate(0, 0, -1)
            py5.rotate(py5.radians(angulo))
            limite = py5.width - 2 * MARGEM_X
            buffer = 20
            with py5.push_style():
                py5.stroke("#000")
                py5.stroke_weight(3)
                py5.rect(-buffer, -buffer, limite + buffer, limite + buffer)
            for x in range(limite, 20, -10):
                with py5.push_style():
                    py5.no_stroke()
                    py5.fill(230 - (x // 4), 100, 50)
                    py5.rect(-buffer, -buffer, x + buffer, x + buffer)
            for x0, y0 in GRADE:
                x = x0 - meio_x
                y = y0 - meio_y
                h = py5.random_int(39, 40)
                s = py5.random_int(94, 95)
                b = py5.random_int(70, 90)
                py5.stroke(h, s, b)
                direcao = py5.random_int(3)
                if direcao == 0:
                    coordenadas = (x, y, x + LARGURA, y + ALTURA)
                elif direcao == 1:
                    coordenadas = (x, y + ALTURA, x + LARGURA, y)
                elif direcao == 2:
                    coordenadas = (x, y, x + LARGURA, y + ALTURA)
                elif direcao == 3:
                    coordenadas = (x, y, x, y + LARGURA)
                py5.line(*coordenadas)
                with py5.push_style():
                    py5.stroke_weight(1)
                    py5.fill(h, s, b)
                    py5.circle(coordenadas[2], coordenadas[3], LARGURA / 2)
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
