"""2026-10-26
Pro dia nascer feliz
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

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
nome_camadas_paleta = "laranja"
nome_paleta = "brasil-03"
celula_largura = 800
celula_altura = 800
meia_largura = celula_largura / 2
meia_altura = celula_altura / 2
proporcoes = (0.8, 0.4)


def inicializa():
    paleta = gera_paleta(nome_paleta, True)
    camadas_paleta = gera_paleta(nome_camadas_paleta, True)
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
    camadas = []
    cores = []
    for _ in range(len(celulas)):
        shuffle(paleta)
        fundo, preenchimento = paleta[0], paleta[1]
        cores.append((paleta[0], paleta[1]))
    shuffle(cores)
    for cor, (idx, x, idy, y) in enumerate(celulas):
        proporcao_base = proporcoes[idy % len(proporcoes)]
        proporcao = min(0.95, max(0, py5.random_gaussian(proporcao_base, 0.2)))
        dimensao = min(celula_largura, celula_altura) * proporcao
        proporcao_max = max(0.95, max(0, py5.random_gaussian(proporcao_base, 0.2)))
        dimensao_max = max(celula_largura, celula_altura) * proporcao_max
        passos = np.linspace(dimensao_max, dimensao, len(camadas_paleta))
        for d in passos:
            camadas.append((d, camadas_paleta[0]))
            camadas_paleta.rotate()
        fundo, preenchimento = cores[cor]
        if idx % 4 == 0:
            fundo, preenchimento = preenchimento, fundo
        grade.append((x, y, dimensao, fundo, preenchimento, camadas))
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
        for xb, yb, dimensao, fundo, preenchimento, camadas in grade:
            x, y = xb + meia_largura, yb + meia_altura
            py5.fill(fundo)
            py5.rect(x, y, celula_largura, celula_altura)
            with py5.push():
                forma.set_fill(False)
                for tamanho, cor in camadas:
                    forma.set_stroke(cor)
                    forma.set_stroke_weight(5)
                    py5.shape(forma, x, y, tamanho, tamanho)
            forma.set_stroke(preenchimento)
            forma.set_stroke_weight(3)
            forma.set_fill(True)
            forma.set_fill(preenchimento)
            py5.shape(forma, x, y, dimensao, dimensao)
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
