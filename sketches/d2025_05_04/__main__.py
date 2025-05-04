"""2025-05-04
Colisões 078
Grades com padrões fabricados
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
    payload = {"traco": 8}
    colecao = [
        padrao(**payload) for padrao in b.Biblioteca.get_categoria("tracos").values()
    ]
    return colecao


def gera_cores_padrao() -> t.CoresPadrao:
    nome_paleta = py5.random_choice(
        [
            "franca-01",
            "italia-01",
            "basco-01",
            "brasil-01",
        ]
    )
    paleta = gera_paleta(nome_paleta)
    preenchimento = py5.random_choice(paleta)
    fundo = None
    traco = py5.random_choice(paleta)
    return t.CoresPadrao(traco, preenchimento, fundo)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    colecao = gera_colecao()
    with py5.push():
        py5.translate(0, 0, -200)
        py5.rect_mode(py5.CORNER)
        py5.fill("#111")
        py5.rect(-py5.width * 2, -py5.height * 2, py5.width * 4, py5.height * 4)
    celulas = 20
    espacamento = 4
    fundo = py5.color("#333")
    borda = t.Borda(fundo, espacamento)
    largura = 1000
    rotacoes = range(0, 360, 45)
    for idz in range(0, 3):
        grade = GradeLinearPadroes(
            largura,
            largura,
            celulas,
            celulas,
            (espacamento, espacamento),
            colecao,
            borda=borda,
        )
        grade_padroes = grade.padroes
        with py5.push():
            py5.translate(0, 0, -10 + idz)
            for celula in grade.celulas:
                cores = gera_cores_padrao()
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
