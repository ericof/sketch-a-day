"""2026-10-22
Hope redux 06 (A plural country)
A grid with Brasil maps.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from random import shuffle
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.grade import cria_grade_ex
from sketches.utils.helpers import recursos as rc
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
nome_paleta = "Warhol"
celula_largura = 200
celula_altura = 80
meia_largura = celula_largura / 2
meia_altura = celula_altura / 2
proporcoes = (0.75, 0.5)


def inicializa():
    paleta = gera_paleta(nome_paleta, True)
    grade = []
    celulas = cria_grade_ex(
        largura=helpers.DIMENSOES.external[0],
        altura=helpers.DIMENSOES.external[1],
        margem_x=0,
        margem_y=0,
        celula_x=celula_largura,
        celula_y=celula_altura,
        alternada=True,
    )
    cores = []
    for _ in range(len(celulas)):
        shuffle(paleta)
        fundo, preenchimento = paleta[0], paleta[1]
        cores.append((paleta[0], paleta[1]))
    shuffle(cores)
    for cor, (idx, x, idy, y) in enumerate(celulas):
        fundo, preenchimento = cores[cor]
        if idx % 4 == 0:
            fundo, preenchimento = preenchimento, fundo
        grade.append((idy, x, y, fundo, preenchimento))
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
        for idy, xb, yb, fundo, preenchimento in grade:
            proporcao = proporcoes[idy % len(proporcoes)]
            dimensao = min(celula_largura, celula_altura) * proporcao
            forma_largura = dimensao
            forma_altura = dimensao
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
    global grade
    key = py5.key
    if key == " ":
        save_and_close()
    elif key == "r":
        grade = inicializa()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
