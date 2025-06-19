"""2025-06-19
Vera Molnár 04
Implementa quadrados concêntricos levemente perturbados
png
Sketch,py5,CreativeCoding
"""

import numpy as np
import py5

from utils import helpers
from utils.draw import cria_grade_ex, gera_paleta

sketch = helpers.info_for_sketch(__file__, __doc__)


def quadrilateros(x, y, tamanho, paleta, rotacao=0):
    py5.no_fill()
    py5.stroke_weight(3)
    paleta.rotate(py5.random_int(0, len(paleta) - 1))
    tamanho_max = tamanho * 0.75
    tamanho_min = tamanho * 0.1
    tamanhos = np.linspace(tamanho_min, tamanho_max, num=7, endpoint=True)
    x += py5.random_int(-15, 15)
    y += py5.random_int(-15, 15)
    for idx, tamanho in enumerate(tamanhos):
        paleta.rotate()
        traco = paleta[0]
        with py5.push_matrix():
            semente = py5.random(0.5, 2.5)
            rot = rotacao * semente
            if idx % 2 == 1:
                rot *= -1

            py5.translate(x, y)
            py5.rotate(py5.radians(rot))
            py5.stroke(traco)
            py5.square(0, 0, tamanho)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background("#DDD")
    py5.rect_mode(py5.CENTER)
    largura = 100
    altura = 100
    paleta = gera_paleta("sunset-ocean", True)
    grade = cria_grade_ex(py5.width * 2, py5.height * 2, 0, 0, largura, altura, True)
    total = len(grade)
    rotacoes = np.logspace(0.001, 0.98, num=total, endpoint=True)
    with py5.push():
        py5.translate(-100, -100, -80)
        for idx, xb, idy, yb in grade:
            index = idy * 8 + idx
            rotacao = rotacoes[index]
            x = xb + largura / 2
            y = yb + altura / 2
            quadrilateros(x, y, 98, paleta, rotacao)
    with py5.push():
        py5.stroke("#FFF")
        helpers.write_legend(sketch=sketch, frame="#FFF", cor="#000")


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
