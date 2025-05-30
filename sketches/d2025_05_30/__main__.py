"""2025-05-30
Bulcão 06
Homenagem a Athos Bulcão.
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
    return [b.Biblioteca.get_padrao("AzulejoCirculoTriangulo")(traco=1)]


def gera_cores_padrao() -> t.CoresPadrao:
    preenchimento = py5.color("#1C8EAF")
    fundo = py5.color("#F87109")
    traco = preenchimento
    return t.CoresPadrao(traco, preenchimento, fundo)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    meio_x = py5.width / 2
    meio_y = py5.height / 2
    cores = gera_cores_padrao()
    preenchimento = cores.preenchimento
    fundo = cores.fundo
    with py5.push():
        py5.translate(meio_x, meio_y, -100)
        py5.fill(fundo)
        py5.rect_mode(py5.CORNERS)
        py5.rect(-py5.width, -py5.height, py5.width, py5.height)
    celulas = 15
    espacamento = 3
    borda = t.Borda(preenchimento, espacamento)
    colecao = gera_colecao()
    grade = GradeLinearPadroes(
        py5.width,
        py5.height,
        celulas,
        celulas,
        (espacamento, espacamento),
        colecao,
        borda=borda,
    )
    grade_padroes = grade.padroes
    rotacoes = [0, 90, 180, 270]
    cores = gera_cores_padrao()
    with py5.push():
        py5.translate(0, 0, -10)
        for celula in grade.celulas:
            padrao = next(grade_padroes)
            rotacao = py5.random_choice(rotacoes)
            celula(padrao, rotacao, cores)
    helpers.write_legend(sketch=sketch, frame="#000", cor="#FFF")


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
