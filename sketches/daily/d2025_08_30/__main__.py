"""2025-08-30
Gradientes poligonais 07
Exercício de criação de polígonos com diferentes tonalidades.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from sketches.padroes.poligonos import gera_poligono_regular
from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color(0, 95)
    py5.background(cor_fundo)
    py5.rect_mode(py5.CORNER)
    py5.shape_mode(py5.CENTER)
    py5.color_mode(py5.HSB, 360, 100, 100)
    passo = 40
    traco = 4
    passo_interno = traco + 1
    forma_largura = passo * 1.5
    forma_altura = passo * 1.5
    formas = []
    for lados in (5, 6):
        rotacao = np.pi / lados
        formas.append(
            gera_poligono_regular(
                lados=lados,
                largura=forma_largura,
                altura=forma_altura,
                rotacao=rotacao,
            )
        )
    buffer = int(forma_largura * 2)
    largura = helpers.DIMENSOES.internal[0] + buffer
    altura = helpers.DIMENSOES.internal[1] + buffer
    x0 = helpers.DIMENSOES.pos_interno[0] - buffer // 2
    y0 = helpers.DIMENSOES.pos_interno[1] - buffer // 2
    xx, yy = np.meshgrid(
        np.arange(0, largura + 1, passo), np.arange(0, altura + 1, passo), indexing="ij"
    )
    pontos = np.column_stack((xx.ravel(), yy.ravel()))
    np.random.shuffle(pontos)
    with py5.push():
        py5.translate(x0, y0, -5)
        py5.blend_mode(py5.BLEND)
        for x, y in pontos:
            forma = py5.random_choice(formas)
            forma.set_fill(False)
            h = py5.random_int(0, 120)
            s = py5.random_int(80, 100)
            b = py5.random_int(80, 100)
            for i in range(int(forma_largura), 0, -passo_interno):
                cor = py5.color(h, s, b)
                forma.set_stroke_weight(traco)
                forma.set_stroke(cor)
                py5.shape(forma, x, y, i, i)
                h = py5.random_int(120, 240)
                s *= 0.85
                b *= 0.95

    # Credits and go
    canvas.sketch_frame(
        sketch, cor_fundo, "large_transparent_white", "transparent_white"
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
