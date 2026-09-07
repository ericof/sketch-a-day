"""2026-09-06
Padrões 02
Exercício de padrões coloridos
ericof.com
png
Sketch,py5,CreativeCoding
"""

from sketches.padroes import biblioteca as b
from sketches.padroes.tipos import CoresPadrao
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.grade import cria_grade
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

paleta = gera_paleta("brasil-03", True)

largura_x = 200
largura_y = 200
traco = 3
angulos = [0, 90, 180, 270, 360]


def inicializa():
    payload = {
        "traco": traco,
        "largura": largura_x * 0.980,
        "altura": largura_y * 0.980,
    }
    padroes = [
        padrao(**payload) for padrao in b.Biblioteca.get_categoria("bulcao").values()
    ]
    posicoes = cria_grade(
        *helpers.DIMENSOES.internal, 0, 0, largura_x, largura_y, False
    )
    grade = []
    for x, y in posicoes:
        padrao = py5.random_choice(padroes)
        cores = CoresPadrao(
            py5.color(paleta[0]),
            py5.color(paleta[1]),
            py5.color(paleta[2]),
        )
        rotacao = float(py5.random_choice(angulos))
        grade.append((x, y, padrao, cores, rotacao))
    return grade


def setup():
    global grade
    py5.size(*helpers.DIMENSOES.external, py5.P2D)
    py5.image_mode(py5.CENTER)
    grade = inicializa()


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, -2)
        for x, y, padrao, cores, rotacao in grade:
            pg = padrao(rotacao, cores)
            py5.image(pg, x + largura_x, y + largura_y)

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
