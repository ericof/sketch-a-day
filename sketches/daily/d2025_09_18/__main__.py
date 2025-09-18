"""2025-09-18
Colorido geométrico redux II
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


LARGURA = 40
ALTURA = 60
LADOS = 4
forma: py5.Py5Shape | None = None


def setup():
    global forma
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.ellipse_mode(py5.CORNER)
    py5.shape_mode(py5.CORNER)
    forma = gera_poligono_regular(lados=LADOS, largura=LARGURA, altura=ALTURA)


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
        for idx, x, idy, y in grade:
            h = 90 + (py5.sin(py5.radians(idx * 4)) * 240) % 360
            s = 100 * py5.cos(py5.radians(idy * 5)) % 100
            b = 100
            cor = py5.color(h, s, b)
            forma.set_fill(cor)
            h -= 360
            s = 100
            traco = py5.color(abs(h), s, b)
            forma.set_stroke(traco)
            py5.shape(forma, x, y)
            with py5.push():
                py5.fill("#FFF")
                py5.stroke("#000")
                py5.stroke_weight(8)
                py5.ellipse(x, y, LARGURA * 0.7, ALTURA * 0.4)
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
