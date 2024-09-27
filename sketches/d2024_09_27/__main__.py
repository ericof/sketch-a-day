"""2024-09-27
Mondrian Redux 04
Releitura 2D de Piet Mondrian
png
Sketch,py5,CreativeCoding,Mondrian
"""

from collections import defaultdict
from random import choice

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

MARGEM = 50
UNIDADE = 5
MAX_UNIDADES = 6
COLUNAS = (helpers.LARGURA - 2 * MARGEM) // UNIDADE
LINHAS = (helpers.ALTURA - 2 * MARGEM) // UNIDADE

MEIO_X = helpers.LARGURA // 2
MEIO_Y = helpers.LARGURA // 2

# Ref: https://www.colourlovers.com/palette/3991914/Mondrians_Crayons
PALETA = [
    "#F7D744",
    "#D0341E",
    "#D0341E",
    "#120D2D",
    "#425AC6",
    "#CAC9D1",
]

CONTAGEM = defaultdict(int)
GRADE = {}


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.color_mode(py5.RGB)
    py5.frame_rate(2)
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            limite = min(MAX_UNIDADES, min(LINHAS - linha, COLUNAS - coluna))
            n = py5.random_int(1, limite)
            for t in range(n, 0, -1):
                if checa_espaco_grade(coluna, linha, t):
                    cria_grade(coluna, linha, t)


def cria_grade(coluna, linha, n):
    CONTAGEM[n] += 1
    for dc in range(n):
        for dl in range(n):
            GRADE[coluna + dc, linha + dl] = 0, 0, 0, 0
    GRADE[coluna, linha] = (n, CONTAGEM[n], py5.random_int(5, 80))


def desenha_quad(coluna, linha, n, altura):
    tamanho = n * UNIDADE
    x = (coluna * UNIDADE + MARGEM) - MEIO_X
    y = (linha * UNIDADE + MARGEM) - MEIO_Y
    with py5.push_style():
        with py5.push_matrix():
            py5.translate(x, y, 0)
            color = py5.color(choice(PALETA))
            py5.stroke(0)
            py5.stroke_weight(1)
            py5.fill(color)
            for z in range(-altura, altura):
                with py5.push_matrix():
                    py5.translate(0, 0, z)
                    py5.circle(0, 0, tamanho)


def checa_espaco_grade(coluna, linha, n) -> bool:
    for dc in range(n):
        for dl in range(n):
            if GRADE.get((coluna + dc, linha + dl)):
                return False
    return True


def draw():
    py5.background(248, 241, 219)
    with py5.push_matrix():
        py5.translate(MEIO_X, MEIO_Y, -200)
        for (coluna, linha), valores in GRADE.items():
            n = valores[0]
            if n:
                altura = valores[2]
                desenha_quad(coluna, linha, n, altura)
    helpers.write_legend(sketch=sketch, cor="#000", frame="#FFF")


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    helpers.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
