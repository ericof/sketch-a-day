"""2025-04-26
Padrões Fabricados 13
Fábrica de padrões utilizando paleta brasileira.
png
Sketch,py5,CreativeCoding
"""

import py5

from padroes import biblioteca as b
from padroes import tipos as t
from padroes.fabrica import GradeLinearPadroes
from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def gera_colecao() -> list[t.Padrao]:
    colecao = []
    padroes = [
        b.Biblioteca.get_padrao("HexagonoRaios"),
        b.Biblioteca.get_padrao("QuadradoRaios"),
        b.Biblioteca.get_padrao("CirculosRaios"),
    ]
    traco = 2
    for padrao in padroes:
        colecao.append(padrao(traco=traco))
    return colecao


def gera_cores_padrao() -> t.CoresPadrao:
    preenchimento = py5.color("#002776")
    fundo = py5.color("#002776")
    traco = py5.color("#FFCC29")
    return t.CoresPadrao(traco, preenchimento, fundo)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    meio_x = py5.width / 2
    meio_y = py5.height / 2

    cores = gera_cores_padrao()
    fundo = cores.preenchimento
    with py5.push():
        py5.translate(meio_x, meio_y, -100)
        py5.fill(fundo)
        py5.rect_mode(py5.CORNERS)
        py5.rect(-py5.width, -py5.height, py5.width, py5.height)
    espacamento = -4
    borda = t.Borda(fundo, espacamento)
    colecao = gera_colecao()
    grade = GradeLinearPadroes(
        1000,
        1000,
        10,
        10,
        (espacamento, espacamento),
        colecao,
        borda=borda,
    )
    grade_padroes = grade.padroes
    rotacoes = range(0, 360, 90)
    with py5.push():
        py5.translate(-100, -100, -10)
        for celula in grade.celulas:
            padrao = next(grade_padroes)
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
