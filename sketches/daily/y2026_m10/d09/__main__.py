"""2026-10-09
Hope 05
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
tamanho_final = 100
passos = 60
limites_traco = (3, 80)
cor_estranha = py5.color("#f71735")


def inicializa() -> list[tuple[int, int, int, int, float, int]]:
    paleta = gera_paleta(nome_paleta, True)
    tamanhos = np.logspace(
        np.log10(tamanho_inicial), np.log10(tamanho_final), num=passos, dtype=int
    )
    camadas = []
    for idx, tamanho in enumerate(tamanhos):
        cor_traco = paleta[0]
        x = (passos - idx) * 10 * -1
        y = (passos - idx) * 10 * 1
        if idx % 13 == 0:
            cor_traco = cor_estranha
        traco = float(
            py5.remap(tamanho, tamanho_final, tamanho_inicial, *limites_traco)
        )
        camadas.append((x, y, idx, tamanho, traco, cor_traco))
        paleta.rotate()
    return camadas


def setup():
    global camadas, forma
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.shape_mode(py5.CENTER)
    forma = rc.carrega_svg_forma("brasil.svg")
    camadas = inicializa()


def draw():
    py5.background(cor_fundo)
    forma.set_fill(False)
    forma.set_stroke_join(py5.ROUND)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, -passos + 2)
        for x, y, z, tamanho, traco, cor_traco in camadas:
            with py5.push():
                py5.translate(0, 0, z)
                forma.set_stroke(cor_traco)
                forma.set_stroke_weight(traco)
                py5.shape(forma, x, y, tamanho, tamanho)
        x, y, z, tamanho, *_ = camadas[-1]
        py5.translate(0, 0, z)
        forma.set_fill(True)
        forma.set_fill(cor_estranha)
        py5.shape(forma, x, y, tamanho, tamanho)
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
