"""2025-07-14
Polígonos e gradientes IV
Exercício de criação de polígonos regulares com gradientes de cores.
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


def cores_vertices(lados: int) -> list[int]:
    """Gera uma lista de cores para os vértices de um polígono."""
    h = py5.random_int(0, 360)
    s = py5.random_int(80, 100)
    b = py5.random_int(80, 100)
    cores = []
    for _ in range(lados):
        cor = py5.color(h, s, b)
        cores.append(cor)
        h = py5.random_int(0, 360)
        s *= 0.85
        b *= 0.9
    return cores


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color(0, 99.8)
    py5.background(cor_fundo)
    py5.rect_mode(py5.CORNER)
    py5.shape_mode(py5.CORNER)
    py5.color_mode(py5.HSB, 360, 100, 100)
    base_largura = 60
    base_altura = 60
    traco = 12
    xc, yc = helpers.DIMENSOES.centro

    with py5.push_matrix():
        py5.translate(xc, yc, -5)
        py5.blend_mode(py5.BLEND)
        for idx, lados in enumerate(range(3, 20)):
            py5.translate(0, 0, -2)
            rotacao = np.pi / lados
            forma_largura = base_largura + idx * 60
            forma_altura = base_altura + idx * 60
            forma = gera_poligono_regular(
                lados=lados,
                largura=forma_largura,
                altura=forma_altura,
                rotacao=rotacao,
            )
            forma.set_fill(False)
            forma.set_stroke_weight(traco)
            cores = cores_vertices(lados)
            forma.set_strokes(cores)
            x = -forma_largura / 2
            y = -forma_altura / 2
            py5.shape(forma, x, y, forma_largura, forma_altura)

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
