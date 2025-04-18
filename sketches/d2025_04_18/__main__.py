"""2025-04-18
Padrões Fabricados 08
Fábrica de padrões de formato quadrado e paleta de duas cores
png
Sketch,py5,CreativeCoding
"""

from random import shuffle

import py5

from padroes import biblioteca as b
from padroes import tipos as t
from padroes.fabrica import GradeLinearPadroes
from utils import helpers
from utils.draw import gera_paleta

sketch = helpers.info_for_sketch(__file__, __doc__)


def gera_colecao() -> list[t.Padrao]:
    payload = {"traco": 0}
    colecao = [
        padrao(**payload) for padrao in b.Biblioteca.get_categoria("quadrados").values()
    ]
    return colecao


def gera_cores_padrao(paleta: list[py5.Py5Color]) -> t.CoresPadrao:
    shuffle(paleta)
    preenchimento = paleta[0]
    fundo = paleta[1]
    traco = paleta[1]
    return t.CoresPadrao(traco, preenchimento, fundo)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    meio_x = py5.width / 2
    meio_y = py5.height / 2
    with py5.push():
        py5.translate(meio_x, meio_y, -100)
        py5.fill("#000")
        py5.rect_mode(py5.CORNERS)
        py5.rect(-py5.width, -py5.height, py5.width, py5.height)
    espacamento = 0
    borda = t.Borda(py5.color("#000"), espacamento)
    colecao = gera_colecao()
    grade = GradeLinearPadroes(
        800,
        800,
        20,
        20,
        (espacamento, espacamento),
        colecao,
        borda=borda,
    )
    paletas = [
        gera_paleta("brasil-02", False),
    ]
    rotacoes = range(0, 360, 90)
    with py5.push():
        py5.translate(0, 0, -10)
        for celula in grade.celulas:
            paleta = paletas[celula.idy % len(paletas)]
            padrao = next(grade.padroes)
            cores = gera_cores_padrao(paleta)
            rotacao = py5.random_choice(rotacoes)
            celula(padrao, rotacao, cores)
    helpers.write_legend(sketch=sketch, frame="#FFF", cor="#000")


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
