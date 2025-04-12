"""2025-04-12
Padrões Fabricados 01
Fábrica de padrões "circulares"
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


def padroes() -> list[t.Padrao]:
    padroes = []

    for padrao, peso in [
        [b.CirculoCanto(traco=2), 20],
        [b.CirculoCentroP(traco=2), 1],
        [b.CirculoCentroM(traco=2), 2],
        [b.CirculoConncentrico(traco=2), 1],
        [b.RaiosCanto(traco=2), 20],
    ]:
        for _ in range(peso):
            padroes.append(padrao)
    return padroes


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    espacamento = 4
    borda = t.Borda(py5.color("#000"), 60)
    grade = GradeLinearPadroes(
        700,
        700,
        8,
        8,
        (espacamento, espacamento),
        padroes(),
        borda=borda,
    )
    paleta_frente = gera_paleta("laranja", True)
    paleta_fundo = gera_paleta("azul", True)
    rotacoes = range(0, 360, 90)
    with py5.push():
        py5.translate(50, 50, -10)
        for celula in grade.celulas:
            padrao = next(grade.padroes)
            cores = t.CoresPadrao(
                py5.color("#000"),
                paleta_frente[0],
                paleta_fundo[0],
            )
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
