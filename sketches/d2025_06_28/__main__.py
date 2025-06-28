"""2025-06-28
Mosaico 09
Mosaico com retângulos vazados em uma grade desigual.
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers
from utils.draw import gera_paleta, grade_desigual

sketch = helpers.info_for_sketch(__file__, __doc__)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    fundo = py5.color(255)
    py5.background(fundo)
    py5.stroke_weight(1)
    py5.stroke(255)
    py5.ellipse_mode(py5.RADIUS)
    paleta = gera_paleta("brasil-03", True)
    grade = grade_desigual(py5.width, py5.height, 800, 6000, 4, 4)
    meio_x = py5.width // 2
    meio_y = py5.height // 2
    with py5.push():
        py5.translate(meio_x, meio_y, -80)
        for xb, yb, largura, altura in grade:
            x = xb - meio_x
            y = yb - meio_y
            cor = paleta[0]
            with py5.push():
                py5.fill(cor)
                py5.rect(x, y, largura, altura)
            paleta.rotate()
            with py5.push():
                x += largura // 2
                y += altura // 2
                cor = paleta[0]
                py5.stroke_weight(1)
                py5.fill(fundo)
                raio = min(largura, altura) / 4
                py5.circle(x, y, raio)
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
