"""2025-07-16
Polígonos e gradientes VI
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


def cores_vertices(lados: int, h_range: tuple[int, int]) -> list[int]:
    """Gera uma lista de cores para os vértices de um polígono."""
    h = py5.random_int(*h_range)
    s = py5.random_int(80, 100)
    b = py5.random_int(80, 100)
    cores = []
    for _ in range(lados):
        cor = py5.color(h, s, b)
        cores.append(cor)
        s *= 0.85
        b *= 0.75
    return cores


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color(0, 99.8)
    py5.background(cor_fundo)
    py5.rect_mode(py5.CORNER)
    py5.shape_mode(py5.CENTER)
    py5.color_mode(py5.HSB, 360, 100, 100)
    inicio = -600
    fim = 600
    forma_largura = 80
    forma_altura = 80
    passo = forma_largura / 1.5
    items = int((fim - inicio) / passo) + 1
    xc, yc = helpers.DIMENSOES.centro
    x_a = np.linspace(inicio, fim, num=items)
    y_a = np.linspace(inicio, fim, num=items)
    with py5.push_matrix():
        py5.translate(xc, yc, -5)
        py5.blend_mode(py5.BLEND)
        for idx, x in enumerate(x_a):
            lados = 6
            traco = 5
            rotacao = np.pi / lados if idx % 2 == 0 else 0
            for y in y_a:
                forma = gera_poligono_regular(
                    lados=lados,
                    largura=forma_largura,
                    altura=forma_altura,
                    rotacao=rotacao,
                )
                forma.set_fill(False)
                forma.set_stroke_weight(traco)
                h_0 = py5.random_int(0, 240)
                h_1 = h_0 + 120
                h_range = (h_0, h_1)
                cores = cores_vertices(lados, h_range)
                forma.set_strokes(cores)
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
