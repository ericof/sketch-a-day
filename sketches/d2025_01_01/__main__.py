"""2025-01-01
Olá 2025
E viva a primeira rotação do ano de 2024
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


MESES = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

ESPECIAIS = (
    (2, 28),
    (3, 3),
    (5, 11),
    (11, 18),
)

MARGEM = 40
PASSO = 20


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CORNER)
    y = MARGEM * 3
    for idy in range(0, 12):
        h = idy * 20 + 30
        s = idy * 20 + 50
        y += PASSO
        colunas = MESES[idy]
        y += 20
        x = 30
        for idx in range(colunas):
            py5.stroke(h, s, 100)
            py5.stroke_weight(2)
            py5.no_fill()
            if idy == 0 and idx == 0:
                py5.fill(h, s, 70)
            elif (idy, idx) in ESPECIAIS:
                py5.stroke(0, 100, 70)
            py5.rect(x, y, PASSO, PASSO)
            x += PASSO + 4

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
