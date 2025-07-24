"""2025-07-24
Polígonos e gradientes XV
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
    s = py5.random_int(80, 100)
    b = py5.random_int(80, 100)
    cores = []
    for _ in range(lados):
        cor = py5.color(h, s, b)
        cores.append(cor)
        h *= 1.05
        h = h_range[0] if h > h_range[1] else h
    return cores


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color(0)
    py5.background(cor_fundo)
    py5.rect_mode(py5.CORNER)
    py5.shape_mode(py5.CENTER)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.blend_mode(py5.BLEND)
    lados = 8
    largura_min = helpers.DIMENSOES.internal[0] // 20
    largura_max = helpers.DIMENSOES.external[0] + 100
    passo = (largura_max - largura_min) // 40
    vertices = helpers.DIMENSOES.vertices_interno
    for idx, d in enumerate(range(largura_min, largura_max, passo)):
        traco = 5
        h0 = (30 * idx) % 270
        h1 = h0 + 90 - py5.random_int(0, 90)
        traco -= 0.5
        for x, y in vertices:
            x -= 10
            y -= 10
            with py5.push():
                py5.translate(x, y, -250)
                cores = cores_vertices(lados, (h0, h1))
                forma = gera_poligono_regular(
                    lados=lados,
                    largura=d,
                    altura=d,
                    rotacao=py5.PI / lados,
                )
                forma.set_fill(False)
                forma.set_stroke_weight(traco)
                forma.set_strokes(cores)
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
