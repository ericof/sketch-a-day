"""2025-05-20
Padrões Fabricados (Redux) 05
Homenagem aos 99 anos de nascimento de Sylvio Luongo.
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
    colecao = [
        padrao(traco=3)
        for nome, padrao in b.Biblioteca.get_categoria("circulos-tracos").items()
        if nome.endswith("RaiosCanto")
    ]
    return colecao


def gera_cores_padrao(reverso: bool = False) -> t.CoresPadrao:
    cor_1 = "#002776"
    cor_2 = "#FFCC29"
    if reverso:
        cor_1, cor_2 = cor_2, cor_1
    preenchimento = py5.color(cor_1)
    fundo = py5.color(cor_2)
    traco = py5.color(cor_1)
    return t.CoresPadrao(traco, preenchimento, fundo)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    meio_x = py5.width / 2
    meio_y = py5.height / 2

    cores = gera_cores_padrao()
    cores_reverso = gera_cores_padrao(True)
    fundo = cores.fundo
    with py5.push():
        py5.translate(meio_x, meio_y, -100)
        py5.fill(fundo)
        py5.rect_mode(py5.CORNERS)
        py5.rect(-py5.width, -py5.height, py5.width, py5.height)
    celulas = 10
    espacamento = 0
    borda = t.Borda(fundo, espacamento)
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
    with py5.push():
        py5.translate(0, 0, -10)
        for idx, celula in enumerate(grade.celulas, start=1):
            padrao = next(grade_padroes)
            rotacao = (idx * 90) % 360
            if idx > 99:
                continue
            cores_ = cores if idx <= 95 else cores_reverso
            celula(padrao, rotacao, cores_)
    helpers.write_legend(sketch=sketch, frame="#009739", cor="#FFF")


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
