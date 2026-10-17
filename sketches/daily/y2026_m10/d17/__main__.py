"""2026-10-17
Hope redux 01
A grid with Brasil maps.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.grade import cria_grade_ex
from sketches.utils.helpers import recursos as rc
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
nome_paleta = "brasil-01"
celula_largura = 100
celula_altura = 100
meia_largura = celula_largura / 2
meia_altura = celula_altura / 2
proporcao = 0.75
forma_largura = celula_largura * proporcao
forma_altura = celula_largura * proporcao


def inicializa():
    paleta = gera_paleta(nome_paleta, True)
    grade = []
    celulas = cria_grade_ex(
        largura=helpers.DIMENSOES.internal[0],
        altura=helpers.DIMENSOES.internal[1],
        margem_x=0,
        margem_y=0,
        celula_x=celula_largura,
        celula_y=celula_altura,
        alternada=False,
    )
    prev_idy = None
    for _, x, idy, y in celulas:
        passo = 1
        if prev_idy is None:
            prev_idy = idy
        elif prev_idy != idy:
            passo = 2
            prev_idy = idy
        fundo = paleta[0]
        preenchimento = paleta[1]
        grade.append((x, y, fundo, preenchimento))
        paleta.rotate(passo)
    return grade


def setup():
    global grade, forma
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CENTER)
    py5.shape_mode(py5.CENTER)
    forma = rc.carrega_svg_forma("brasil.svg")
    grade = inicializa()


def draw():
    py5.background(cor_fundo)
    forma.set_stroke_join(py5.ROUND)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, -1)
        for xb, yb, fundo, preenchimento in grade:
            x, y = xb + meia_largura, yb + meia_altura
            py5.fill(fundo)
            py5.rect(x, y, celula_largura, celula_altura)
            forma.set_stroke(preenchimento)
            forma.set_stroke_weight(3)
            forma.set_fill(preenchimento)
            py5.shape(forma, x, y, forma_largura, forma_altura)
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
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
