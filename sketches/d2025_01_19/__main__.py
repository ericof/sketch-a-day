"""2025-01-19
Op Art
Exercício de criação de ilusão de ótica
png
Sketch,py5,CreativeCoding,genuary,genuary2025,genuary19
"""

from collections import deque

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

PALETA = deque(
    [
        "#FFF",
        "#CCC",
        "#666",
        "#222",
        "#000",
    ]
)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.rect_mode(py5.CENTER)
    py5.blend_mode(py5.DIFFERENCE)
    meio_w = py5.width // 2
    meio_h = py5.height // 2
    diametros = range(py5.width + 30, -1, -5)
    with py5.push_style():
        py5.no_stroke()
        with py5.push_matrix():
            py5.translate(meio_w, meio_h, -20)
            for diametro in diametros:
                py5.rotate_z(py5.radians(15))
                cor = PALETA[0]
                PALETA.rotate()
                py5.fill(cor)
                py5.rect(0, 0, diametro, diametro)
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
