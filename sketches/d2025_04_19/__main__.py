"""2025-04-19
Padrões Fabricados 09
Fábrica de padrões com traços e paleta basca.
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
    payload = {"traco": 5}
    colecao = [
        padrao(**payload) for padrao in b.Biblioteca.get_categoria("tracos").values()
    ]
    return colecao


def gera_cores_padrao(paleta: list[py5.Py5Color]) -> t.CoresPadrao:
    fundo = paleta[1]
    traco = paleta[2]
    return t.CoresPadrao(traco, fundo, fundo)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    meio_x = py5.width / 2
    meio_y = py5.height / 2
    paleta = gera_paleta("basco-01", False)
    fundo = paleta[2]
    with py5.push():
        py5.translate(meio_x, meio_y, -100)
        py5.fill(fundo)
        py5.rect_mode(py5.CORNERS)
        py5.rect(-py5.width, -py5.height, py5.width, py5.height)
    espacamento = 5
    borda = t.Borda(fundo, espacamento)
    colecao = gera_colecao()
    grade = GradeLinearPadroes(
        800,
        800,
        10,
        10,
        (espacamento, espacamento),
        colecao,
        borda=borda,
    )
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
