"""2025-02-28
Rotatio XIV
Rotações de retângulos com paleta em tons de azul
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers
from utils.draw import gera_paleta

sketch = helpers.info_for_sketch(__file__, __doc__)

PASSO = 0.92


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CENTER)
    py5.blend_mode(py5.BLEND)
    paleta = gera_paleta("azul", True)
    quarto_w = py5.width / 4
    terco_h = py5.height / 3
    r = -38
    direcao = 1
    diametro = 2 * py5.width
    tamanho_paleta = len(paleta)
    razao_larg_alt = 0.75
    voltas = 18
    desvio_x = 2
    desvio_y = 2
    angulo_final = voltas * 360
    with py5.push_style():
        py5.no_stroke()
        with py5.push_matrix():
            py5.translate(quarto_w, terco_h, -20)
            idx = 0
            while diametro > 30:
                if idx and idx % tamanho_paleta == 0:
                    direcao *= -1
                    r += 5
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
