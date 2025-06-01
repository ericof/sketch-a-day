"""2025-06-01
Bulcão 08
Homenagem a Athos Bulcão.
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
    return [
        padrao(traco=1)
        for padrao in b.Biblioteca.get_categoria("bulcao_tres_tracos").values()
    ]


def gera_cores_padrao() -> t.CoresPadrao:
    paleta = gera_paleta("mondrian")
    preenchimento = py5.random_choice(paleta)
    fundo = None
    while not fundo or fundo == preenchimento:
        fundo = py5.random_choice(paleta)
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
    with py5.push():
        py5.translate(0, 0, -10)
        for celula in grade.celulas:
            cores = gera_cores_padrao()
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
