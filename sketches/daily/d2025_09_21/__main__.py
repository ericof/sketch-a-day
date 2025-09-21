"""2025-09-21
Colorido geométrico redux V
Losangos distribuídos em uma grade, com cores baseadas em senoides e cossenoides.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from sketches.padroes.poligonos import gera_poligono_regular
from sketches.utils.draw import canvas
from sketches.utils.draw.grade import cria_grade_ex
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)


LARGURA = 60
ALTURA = 20
LADOS = 6
forma: py5.Py5Shape | None = None


def setup():
    global forma
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.ellipse_mode(py5.CORNER)
    py5.shape_mode(py5.CORNER)
    forma = gera_poligono_regular(lados=LADOS, largura=LARGURA, altura=LARGURA)


def draw():
    cor_fundo = py5.color(0)
    py5.background(cor_fundo)
    grade = cria_grade_ex(
        largura=py5.width,
        altura=py5.height,
        margem_x=0,
        margem_y=0,
        celula_x=LARGURA,
        celula_y=ALTURA,
        alternada=True,
    )
    if forma is not None:
        forma.set_stroke_weight(5)
        forma.set_fill(False)
        for idx, x, idy, y in grade:
            h = 120 + (py5.cos(py5.radians(idy + idx)) * 120)
            s = 100
            b = 80
            cor = py5.color(h, s, b)
            forma.set_stroke(cor)
            py5.shape(forma, x, y)
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
