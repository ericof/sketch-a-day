"""2025-08-06
Colorido geométrico V
Hexágonos distribuídos em uma grade, com cores baseadas em senoides e cossenoides.
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


LARGURA = 30
ALTURA = 30
LADOS = 6
forma: py5.Py5Shape | None = None


def setup():
    global forma
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.shape_mode(py5.CORNER)
    forma = gera_poligono_regular(
        lados=LADOS, largura=LARGURA, altura=ALTURA, rotacao=py5.PI / LADOS
    )


def cores_posicao(idx, idy) -> tuple[int, int | bool]:
    """Calcula as cores baseadas na posição da grade."""
    h = 80
    s = 100
    b = 100 - (py5.sin(idx * 0.1) * 60)
    preenchimento = py5.color(h, s, b)
    h -= 360
    s -= py5.sin(idy * 0.1) * 100
    traco = py5.color(abs(h), abs(s), abs(b))
    return preenchimento, traco


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
    linhas = py5.height // ALTURA
    meio = linhas // 2
    if forma is not None:
        forma.set_stroke_weight(2)
        for idx, x, idy, y in grade:
            preenchimento, traco = cores_posicao(idx, idy)
            forma.set_fill(preenchimento)
            forma.set_stroke(traco)
            z = (30 * ((idy - meio) / meio)) - 30
            with py5.push():
                py5.translate(x, y, z)
                # Desenho da forma
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
