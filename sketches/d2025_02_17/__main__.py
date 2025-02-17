"""2025-02-17
Rotatio III
Rotações de retângulos com paleta em tons de laranja
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers
from utils.draw import gera_paleta

sketch = helpers.info_for_sketch(__file__, __doc__)

PASSO = 0.95


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CENTER)
    # py5.blend_mode(py5.DIFFERENCE)
    paleta = gera_paleta("laranja", True)
    tamanho_paleta = len(paleta)
    meio_w = py5.width // 2
    meio_h = py5.height // 2
    r = -15
    direcao = 1
    diametro = 2 * py5.width
    with py5.push_style():
        py5.no_stroke()
        with py5.push_matrix():
            py5.translate(meio_w, meio_h, -20)
            idx = 0
            while diametro > 10:
                angulo = 0
                cor = paleta[0]
                paleta.rotate(direcao)
                py5.fill(cor)
                while angulo < 720:
                    if idx and not (idx % tamanho_paleta):
                        direcao *= -1
                        r *= direcao
                    py5.rotate_z(py5.radians(r))
                    altura = diametro
                    py5.rect(0, 0, diametro, altura)
                    angulo += abs(r)
                diametro *= PASSO
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
