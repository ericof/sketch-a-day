"""2026-05-29
Planning Session 02
Lembranças de um planejamento com post its
ericof.com|https://ericof.com/en/sketches/2024-10-19
png
Sketch,py5,CreativeCoding
"""

from random import shuffle
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.grade import cria_grade
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

celula_x = 80
celula_y = 80
largura_base = 70
altura_base = 70
traco_peso_min = 4
traco_peso_max = 6
GRADE: list[tuple[tuple[float, float], py5.Py5Shape]] = []


def calcula_grade() -> list[tuple[tuple[float, float], py5.Py5Shape]]:
    """Monta as formas da grade posicionadas sobre a area interna do canvas.

    Para cada ponto da grade (embaralhada) cria um retangulo com cor de
    preenchimento sorteada da paleta ``Navy-Orange``, traco preto de peso
    aleatorio, escala aleatoria e rotacao que cresce conforme a posicao
    ``x``/``y`` do ponto.

    :returns: pares ``((x, y), forma)`` com a posicao e a forma a desenhar.
    """
    grade = []
    paleta = gera_paleta("Navy-Orange", False)
    pontos = cria_grade(*helpers.DIMENSOES.internal, 0, 0, celula_x, celula_y, False)
    shuffle(pontos)
    for x, y in pontos:
        cor_interna = py5.color(py5.random_choice(paleta))
        traco = py5.color("#000")
        peso = py5.random_int(traco_peso_min, traco_peso_max)
        mult = py5.random(1.2, 1.5)
        largura = largura_base * mult
        altura = altura_base * mult
        rotacao_max = float(
            py5.remap(y, -200, 1000, 0, 15) + py5.remap(x, -200, 1000, 0, 2)
        )
        rotacao = float(py5.radians(py5.random(-rotacao_max, rotacao_max)))
        forma = py5.create_shape(py5.RECT, 0, 0, largura, altura)
        forma.set_stroke(traco)
        forma.set_stroke_weight(peso)
        forma.set_fill(cor_interna)
        forma.rotate(rotacao)
        grade.append(((x, y), forma))
    return grade


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.rect_mode(py5.CORNER)
    GRADE.extend(calcula_grade())


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, 0)
        for (x, y), forma in GRADE:
            py5.shape(forma, x, y)
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
