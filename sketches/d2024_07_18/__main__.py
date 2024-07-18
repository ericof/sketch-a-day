"""2024-07-18
Memórias 8-bit - Interferência (10)
Círculos desenhados a partir dos cantos do canvas.
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P2D)
    py5.background(40, 40, 40)
    py5.ellipse_mode(py5.CORNER)
    py5.no_fill()
    meio_w = py5.width / 2
    meio_h = py5.height / 2
    for angulo in range(0, 361, 15):
        with py5.push_matrix():
            py5.translate(meio_w, meio_h)
            py5.rotate(py5.radians(angulo))
            for idx, raio in enumerate(range(20, 600, 30)):
                diametro = raio * 2
                if idx % 2 == 1:
                    cor = py5.color(51, 255, 51)
                else:
                    cor = py5.color(255, 176, 0)
                py5.stroke(cor)
                py5.ellipse(-meio_w, -meio_h - raio, diametro, diametro)

    py5.stroke("#000")
    helpers.write_legend(sketch=sketch, frame="#000")


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
