"""2025-11-13
Pastel Squares
Exercício de criação de múltiplos quadrados rotacionados com cores pastéis.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)


def draw():
    cor_fundo = py5.color(0)
    py5.background(cor_fundo)
    vertices = helpers.DIMENSOES.vertices_interno
    paleta = gera_paleta("pastel", True)

    for x, y in vertices:
        with py5.push():
            py5.translate(x, y, -10)
            py5.no_fill()
            py5.rect_mode(py5.CENTER)
            for idx, d in enumerate(range(40, 600, 30)):
                with py5.push():
                    py5.rotate(py5.radians(idx * 15))
                    cor = paleta[0]
                    stroke_weight = 2 + ((idx // 4) * 2)
                    py5.stroke_weight(stroke_weight)
                    py5.stroke(cor)
                    py5.square(0, 0, d)
                    paleta.rotate(1)
    x, y = helpers.DIMENSOES.centro
    with py5.push():
        py5.translate(x, y, -10)
        py5.no_fill()
        for idx, d in enumerate(range(5, 300, 15)):
            cor = paleta[0]
            py5.rotate(py5.radians(idx * 15))
            stroke_weight = 2 + ((idx // 4) * 2)
            py5.stroke_weight(stroke_weight)
            py5.stroke(cor)
            py5.square(0, 0, d)
            paleta.rotate(1)

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
