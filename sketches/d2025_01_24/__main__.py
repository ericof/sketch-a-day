"""2025-01-24
Geometric art
Usando apenas retângulos
png
Sketch,py5,CreativeCoding,genuary2025,genuary24
"""

import py5

from utils import helpers
from utils.draw import cria_grade

sketch = helpers.info_for_sketch(__file__, __doc__)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CENTER)
    lg = 80
    al = 40
    lg_p = lg // 2
    al_p = al // 2
    grade = cria_grade(py5.width, py5.height, 0, 0, lg, al, False)
    for x, y in grade:
        direcao = 30 if (x // lg) % 2 else -30
        largura = 5 if (y // al) % 2 else 10
        x += lg_p
        y += al_p
        h = py5.random_gaussian(140, 50)
        s = 80
        b = 90
        py5.fill(h, s, b)
        with py5.push_matrix():
            py5.translate(x, y, -60)
            py5.rotate_z(py5.radians(direcao))
            py5.rect(0, 0, lg, largura)

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
