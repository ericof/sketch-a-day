"""2025-01-13
Triangles and nothing else
Grade com triângulos
png
Sketch,py5,CreativeCoding,genuary,genuary2025,genuary13
"""

from collections import deque
from random import shuffle

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


MARGEM = 200

PALETA = deque(
    [
        "#155E95",
        "#6A80B9",
        "#F6C794",
        "#FFF6B3",
        "#FBF5DD",
        "#A6CDC6",
        "#16404D",
        "#DDA853",
        "#2E5077",
        "#4DA1A9",
        "#79D7BE",
    ]
)


def triangulos():
    meio = py5.width / 2
    x0 = MARGEM
    x1 = py5.width - MARGEM
    y0 = MARGEM
    y1 = py5.width - MARGEM
    coordenadas = [
        ((x0, y0, 0, y0, 0, meio), 1),
        ((x0, y1, 0, y1, 0, meio), 1),
        ((x1, y0, py5.width, y0, py5.width, meio), 1),
        ((x1, y1, py5.width, y1, py5.width, meio), 1),
        ((x0, y0, x1, y0, meio, meio), 1),
        ((x0, y0, x0, y1, 0, meio), 1),
        ((x1, y0, x1, y1, py5.width, meio), 1),
        ((x0, y1, x1, y1, meio, meio), 1),
        ((x0, y0, meio, meio, x0, y1), 1),
        ((x1, y0, meio, meio, x1, y1), 1),
    ]
    for diff in range(0, int(meio - x0)):
        coordenadas.extend(
            [
                ((x0, y0, x1, y0, meio, meio - diff), 4),
                ((x1, y1, py5.width, y1, py5.width, meio - diff), 3),
            ]
        )
    return coordenadas


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    altura = py5.height
    meio = py5.height // 2
    shuffle(PALETA)
    params = triangulos()
    py5.stroke_weight(5)
    for y in range(-2 * altura, 2 * altura + 1, meio):
        with py5.push_matrix():
            py5.translate(0, y, -80)
            for coordenadas, grossura in params:
                py5.stroke_weight(grossura)
                py5.stroke(PALETA[0])
                PALETA.rotate()
                py5.fill(PALETA[0])
                PALETA.rotate()
                py5.triangle(*coordenadas)
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
