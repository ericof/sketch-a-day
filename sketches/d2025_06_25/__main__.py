"""2025-06-25
Mosaico 06
Mosaico com retângulos em uma grade
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers
from utils.draw import gera_paleta, grade_desigual

sketch = helpers.info_for_sketch(__file__, __doc__)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(255)
    py5.stroke_weight(2)
    py5.stroke(255)
    paleta = gera_paleta("mondrian", True)
    grade = grade_desigual(py5.width, py5.height, 3200, 6000, 4)
    meio_x = py5.width // 2
    meio_y = py5.height // 2
    with py5.push():
        py5.translate(meio_x, meio_y, -80)
        for x, y, largura, altura in grade:
            cor = paleta[0]
            py5.fill(cor)
            x -= meio_x
            y -= meio_y
            py5.rect(x, y, largura, altura)
            paleta.rotate()
    helpers.write_legend(sketch=sketch, frame="#000", cor="#fff")


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
