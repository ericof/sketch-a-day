"""2025-02-24
Rotatio X
Rotações de retângulos com paleta em tons de azul e laranja
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers
from utils.draw import gera_paleta

sketch = helpers.info_for_sketch(__file__, __doc__)

PASSO = 0.93


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CENTER)
    py5.blend_mode(py5.BLEND)
    paleta = gera_paleta("sunset-ocean", True)
    meio_w = py5.width // 2
    meio_h = py5.height // 2
    r = -30
    direcao = -1
    diametro = 2 * py5.width
    tamanho_paleta = len(paleta)
    razao_larg_alt = 0.9
    voltas = 5
    desvio_x = 8
    desvio_y = 10
    angulo_final = voltas * 360
    with py5.push_style():
        py5.no_stroke()
        with py5.push_matrix():
            py5.translate(meio_w, meio_h, -20)
            idx = 0
            while diametro > 10:
                if idx and idx % tamanho_paleta == 0:
                    direcao *= -1
                if idx % 20 == 19:
                    r += 3
                angulo = 0
                cor = paleta[tamanho_paleta // 2]
                paleta.rotate(direcao)
                py5.fill(cor)
                while angulo < angulo_final:
                    py5.rotate_z(py5.radians(r))
                    altura = diametro * razao_larg_alt
                    py5.rect(desvio_x, desvio_y, diametro, altura)
                    angulo += abs(r)
                idx += 1
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
