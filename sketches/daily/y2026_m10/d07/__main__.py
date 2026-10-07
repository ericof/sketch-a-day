"""2026-10-07
Hope 03
A shrinking map of Brazil -- with z, because the version with s is already gone
ericof.com
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import recursos as rc
from sketches.utils.helpers import sketches as helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
nome_paleta = "brasil-03"
tamanho_inicial = 4000
tamanho_final = 10
tamanhos = np.logspace(
    np.log10(tamanho_inicial), np.log10(tamanho_final), num=80, dtype=int
)
limites_traco = (1, 120)
baguncinha = (0.2, 0, 0.2)
cor_estranha = py5.color("#f71735")


def setup():
    global forma
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.shape_mode(py5.CENTER)
    forma = rc.carrega_svg_forma("brasil.svg")


def draw():
    py5.background(cor_fundo)
    forma.set_fill(False)
    forma.set_stroke_join(py5.ROUND)
    paleta = gera_paleta(nome_paleta, True)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, -40)
        for idx, tamanho in enumerate(tamanhos):
            cor_traco = paleta[0]
            match idx % 3:
                case 0:
                    x = -baguncinha[0]
                    y = -baguncinha[0]
                case 1:
                    x = baguncinha[1]
                    y = baguncinha[1]
                case 2:
                    x = baguncinha[2]
                    y = baguncinha[2]
            if idx % 25 == 0:
                cor_traco = cor_estranha
            forma.set_stroke(cor_traco)
            traco = float(
                py5.remap(tamanho, tamanho_final, tamanho_inicial, *limites_traco)
            )
            forma.set_stroke_weight(traco)
            py5.shape(forma, x, y, tamanho, tamanho)
            paleta.rotate()
        forma.set_fill(True)
        forma.set_fill(paleta[0])
        py5.shape(forma, 0, 0, tamanho_final, tamanho_final)
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
