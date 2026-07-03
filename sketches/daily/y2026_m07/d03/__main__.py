"""2026-07-03
Recursive Squares 01
Desenha quadrados recursivamente
ericof.com
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

AREAS = [
    (200, 200, 375, gera_paleta("laranja-01", True)),
    (600, 600, 375, gera_paleta("laranja-02", True)),
    (200, 600, 375, gera_paleta("tons-azul-01", True)),
    (600, 200, 375, gera_paleta("pycon-colombia-2025", True)),
]


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CENTER)


def desenha_quadrados(
    cx: float, cy: float, tamanho_base: float, paleta: deque[int], angulo: int = 0
):
    for idx, angulo in enumerate(range(0, 75, 5)):
        tamanho = tamanho_base * (1 - (angulo / 70)) if idx else tamanho_base
        cor = paleta[0]
        paleta.rotate()
        with py5.push():
            py5.translate(cx, cy, -10)
            py5.rotate(py5.radians(angulo))
            py5.stroke(cor)
            py5.square(0, 0, tamanho)


def draw():
    py5.background(cor_fundo)
    py5.no_fill()
    py5.stroke_weight(2)
    py5.stroke("#FFF")
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, -10)
        for cx, cy, tamanho_base, paleta in AREAS:
            desenha_quadrados(cx, cy, tamanho_base, paleta)

    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
