"""2025-07-19
Polígonos e gradientes X
Exercício de criação de polígonos regulares com gradientes de cores.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from sketches.padroes.poligonos import gera_poligono_regular
from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)


def cores_vertices(lados: int, h_range: tuple[int, int]) -> list[int]:
    """Gera uma lista de cores para os vértices de um polígono."""
    h = py5.random_int(*h_range)
    cores = []
    for _ in range(lados):
        s = py5.random_int(80, 100)
        b = py5.random_int(80, 100)
        cor = py5.color(h, s, b)
        cores.append(cor)
        h *= 1.05
        h = h_range[0] if h > h_range[1] else h
    return cores


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color(0, 99.8)
    py5.background(cor_fundo)
    py5.rect_mode(py5.CORNER)
    py5.shape_mode(py5.CENTER)
    py5.color_mode(py5.HSB, 360, 100, 100)
    lados = 15
    traco = 10
    passo = 30
    xc, yc = helpers.DIMENSOES.centro
    with py5.push_matrix():
        py5.translate(xc, yc, -5)
        py5.blend_mode(py5.BLEND)
        for d in range(helpers.DIMENSOES.external[0], 20, -passo):
            cores = cores_vertices(lados, (220, 280))
            forma = gera_poligono_regular(
                lados=lados,
                largura=d,
                altura=d,
                rotacao=0,
            )
            forma.set_fill(False)
            forma.set_stroke_weight(traco)
            forma.set_strokes(cores)
            with py5.push_matrix():
                py5.translate(0, 0, -10)
                py5.shape(forma, 0, 0)

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
