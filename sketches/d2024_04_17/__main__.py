"""2024-04-17
World Plone Day 2024
Uma humilde homenagem a essa comunidade tão generosa.
png
Sketch,py5,CreativeCoding,wpd2024,Plone
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

plone_color = py5.color("#0083BE")


def logo():
    diametro = 600
    diametro_interno = 130
    with py5.push_matrix():
        py5.translate(py5.width / 2, py5.height / 2)
        py5.stroke_weight(2)
        py5.stroke(plone_color)
        py5.no_fill()
        passo = 6
        # Borda
        for i in range(477, diametro + 1, passo):
            py5.circle(0, 0, i)

        passo = 5
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
    py5.size(helpers.LARGURA, helpers.ALTURA)
    py5.background(255)
    logo()
    helpers.write_legend(sketch=sketch, cor=plone_color)


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
