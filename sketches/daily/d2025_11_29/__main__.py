"""2025-11-29
Polígonos -> Polígonos 11
Exercício de criação de polígonos de diversos tamanhos.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from random import shuffle
from sketches.padroes.poligonos import gera_poligono_regular
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
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
    paletas = deque([
        gera_paleta("pastel", True),
        gera_paleta("pastel", True),
    ])
    passo = 50
    traco = 5
    passo_interno = traco * 7
    forma_largura = passo * 1.3
    forma_altura = passo * 1.3
    formas = deque()
    for lados in range(3, 20):
        rotacao = np.pi / lados
        formas.append(
            gera_poligono_regular(
                lados=lados,
                largura=forma_largura,
                altura=forma_altura,
                rotacao=rotacao,
            )
        )
    buffer = int(forma_largura * 6)
    largura = helpers.DIMENSOES.internal[0] + buffer
    altura = helpers.DIMENSOES.internal[1] + buffer
    x0 = helpers.DIMENSOES.pos_interno[0] - buffer // 2
    y0 = helpers.DIMENSOES.pos_interno[1] - buffer // 2
    xx, yy = np.meshgrid(
        np.arange(0, largura + 1, passo), np.arange(0, altura + 1, passo), indexing="ij"
    )
    pontos = np.column_stack((xx.ravel(), yy.ravel()))
    np.random.shuffle(pontos)
    todos_tamanhos = list(range(int(forma_largura), 0, -passo_interno))
    with py5.push_matrix():
        py5.translate(x0, y0, -5)
        py5.blend_mode(py5.BLEND)
        for xb, yb in pontos:
            x = xb + py5.random_int(-5, 5)
            y = yb + py5.random_int(-5, 5)
            forma = formas[0]
            forma.set_fill(False)
            paletas.rotate(py5.random_int(0, len(paletas) - 1))
            tamanhos = todos_tamanhos.copy()
            shuffle(tamanhos)
            elementos = py5.random_int(1, 4)
            for i in tamanhos[:elementos]:
                paleta = paletas[0]
                cor = paleta[0]
                forma.set_stroke_weight(traco)
                forma.set_stroke(cor)
                py5.shape(forma, x, y, i, i)
                paleta.rotate(1)
                paletas.rotate(1)
            formas.rotate(-1)

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
