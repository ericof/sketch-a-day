"""2026-03-31
Language 04
Grade com padrões de traços e círculos. Infelizmente, Luciano, eu ainda não consigo colocar o código no alt-text.
ericof.com
png
Sketch,py5,CreativeCoding
"""  # noQA: E501

from collections.abc import Sequence
from random import shuffle
from sketches.padroes import biblioteca as b
from sketches.padroes import tipos as t
from sketches.padroes.fabrica import GradeLinearPadroes
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.cores.paletas import lista_paletas
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
celula_fundo = py5.color("#CCC")
celulas = 10
espacamento = 2
traco = 5
fundo = py5.color("#222")
borda = t.Borda(fundo, espacamento)

CELULAS: list[tuple[t.Celula, tuple[t.Padrao, float, t.CoresPadrao, float]]] = []


def gera_colecao(largura: float, altura: float) -> list[t.Padrao]:
    """Cria instâncias de todos os padrões da categoria "tracos".

    :param largura: Largura de cada padrão em pixels.
    :param altura: Altura de cada padrão em pixels.
    :returns: Lista de instâncias de :class:`t.Padrao`.
    """
    payload = {"traco": traco, "largura": largura, "altura": altura}
    colecao = [
        padrao(**payload) for padrao in b.Biblioteca.get_categoria("tracos").values()
    ]
    return colecao


def gera_paletas() -> tuple[Sequence[int | str], ...]:
    """Carrega as paletas de cores usadas no sketch.

    :returns: Tupla com paletas que comecem com `op-`.
    """
    paletas = []
    nomes_paletas = [nome for nome in lista_paletas() if nome.startswith("op-")]
    for nome in nomes_paletas:
        paletas.append(gera_paleta(nome))
    shuffle(paletas)
    return tuple(paletas)


PALETAS = gera_paletas()


def gera_cores_padrao(idy: int) -> t.CoresPadrao:
    """Sorteia cores distintas de uma paleta para um padrão.

    :param idy: Índice da linha que estamos utilizando.
    :returns: :class:`t.CoresPadrao` com traço e preenchimento distintos
        e diferentes de branco.
    """
    paleta_id = idy % len(PALETAS)
    paleta = PALETAS[paleta_id]
    fundo = None
    valida = False
    while not valida:
        preenchimento = py5.random_choice(paleta)
        traco = py5.random_choice(paleta)
        valida = preenchimento != traco != celula_fundo
    return t.CoresPadrao(traco, preenchimento, fundo)


def calcula_celulas(
    largura: float,
    altura: float,
    celulas_x: int,
    celulas_y: int,
    espacamento_x: int,
    espacamento_y: int,
    colecao: list[t.Padrao],
    borda: t.Borda | None,
) -> list[tuple[t.Celula, tuple[t.Padrao, float, t.CoresPadrao, float]]]:
    """Calcula células e associa padrões, rotações e cores para cada camada.

    Gera 3 camadas sobrepostas (``idz`` 0-2) com profundidades z distintas.
    As cores são sorteadas por linha (``celula.idy``), usando paletas ``op-``.

    :param largura: Largura total da grade em pixels.
    :param altura: Altura total da grade em pixels.
    :param celulas_x: Número de colunas da grade.
    :param celulas_y: Número de linhas da grade.
    :param espacamento_x: Espaçamento horizontal entre células em pixels.
    :param espacamento_y: Espaçamento vertical entre células em pixels.
    :param colecao: Instâncias de padrões disponíveis para sorteio.
    :param borda: Borda opcional a aplicar em cada célula.
    :returns: Lista de tuplas ``(celula, (padrao, rotacao, cores, z))``.
    """
    celulas = []
    rotacoes = range(0, 360, 45)
    for idz in range(0, 3):
        grade = GradeLinearPadroes(
            largura,
            altura,
            celulas_x,
            celulas_y,
            (espacamento_x, espacamento_y),
            colecao,
            borda=borda,
        )
        grade_padroes = grade.padroes
        z = -10 + idz
        for celula in grade.celulas:
            cores = gera_cores_padrao(celula.idy)
            if idz == 0:
                cores.fundo = celula_fundo
            padrao = next(grade_padroes)
            rotacao = py5.random_choice(rotacoes)
            celulas.append((celula, (padrao, rotacao, cores, z)))
    return celulas


def inicializa_celulas():
    """Calcula as células e suas associações de padrões, rotações e cores."""
    global CELULAS
    py5.window_title("Regenerando células...")
    largura, altura = helpers.DIMENSOES.internal
    colecao = gera_colecao(largura / celulas, altura / celulas)
    CELULAS = calcula_celulas(
        largura, altura, celulas, celulas, espacamento, espacamento, colecao, borda
    )
    py5.window_title("Células regeneradas")


def setup():
    """Inicializa o sketch: cria a janela, calcula grade e padrões."""
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.background(cor_fundo)
    inicializa_celulas()


def draw():
    """Renderiza todas as células e adiciona os créditos do sketch."""
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno)
        for celula, (padrao, rotacao, cores, z) in CELULAS:
            celula(padrao, rotacao, cores, z=z)
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def key_pressed():
    """Captura teclas: ``espaço`` salva e fecha o sketch."""
    key = py5.key
    if key == "r":
        inicializa_celulas()
    elif key == " ":
        save_and_close()


def save_and_close():
    """Para o loop, salva a imagem do sketch e encerra."""
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
