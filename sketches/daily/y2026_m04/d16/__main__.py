"""2026-04-16
World Plone Day 2026
Just a celebration of Plone.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
plone_color = py5.color("#0083BE")


def logo():
    diametro = 600
    diametro_interno = 130
    py5.stroke_weight(2)
    py5.stroke(plone_color)
    py5.no_fill()
    passo = 8
    # Borda
    for i in range(477, diametro + 1, passo):
        py5.circle(0, 0, i)

    passo = 6
    # Circulo 1
    for i in range(0, diametro_interno + 1, passo):
        py5.circle(93, 0, i)
    x = -40
    y = 131
    # Circulo 2
    for i in range(0, diametro_interno + 1, passo):
        py5.circle(x, -y, i)
    # Circulo 3
    for i in range(0, diametro_interno + 1, passo):
        py5.circle(x, y, i)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro)
        logo()
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
