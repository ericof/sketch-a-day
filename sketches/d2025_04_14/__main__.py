"""2025-04-14
Padrões Fabricados 04
Fábrica de padrões brasileiros
png
Sketch,py5,CreativeCoding
"""

import py5

from padroes import biblioteca as b
from padroes import tipos as t
from padroes.fabrica import GradeLinearPadroes
from utils import helpers
from utils.draw import gera_paleta

sketch = helpers.info_for_sketch(__file__, __doc__)


def gera_colecao() -> list[t.Padrao]:
    colecao = []

    for padrao, peso in [
        [b.CirculoCanto(traco=0), 20],
        [b.CirculoCentroP(traco=0), 20],
        [b.TrianguloMetades(traco=0), 5],
        [b.TrianguloCanto(traco=0), 40],
        [b.TrianguloCantoDividido(traco=0), 15],
    ]:
        for _ in range(peso):
            colecao.append(padrao)
    return colecao


def gera_cores_padrao(paleta: list[py5.Py5Color]) -> t.CoresPadrao:
    preenchimento = None
    fundo = None
    traco = None
    while not len({preenchimento, fundo, traco}) == 3:
        preenchimento = py5.random_choice(paleta)
        fundo = py5.random_choice(paleta)
        traco = py5.random_choice(paleta)
    return t.CoresPadrao(traco, preenchimento, fundo)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    espacamento = 2
    borda = t.Borda(py5.color("#444"), 120)
    colecao = gera_colecao()
    grade = GradeLinearPadroes(
        800,
        800,
        8,
        8,
        (espacamento, espacamento),
        colecao,
        borda=borda,
    )
    paleta = gera_paleta("brasil-01", False)
    rotacoes = range(0, 360, 90)
    with py5.push():
        py5.translate(0, 0, -10)
        for celula in grade.celulas:
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
