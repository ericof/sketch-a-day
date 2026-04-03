"""2026-04-03
Language 07
Grade com padrões de traços e círculos.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from collections.abc import Sequence
from dataclasses import dataclass
from random import shuffle
from sketches.padroes import biblioteca as b
from sketches.padroes import tipos as t
from sketches.padroes.fabrica import GradeLinearPadroes
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
celula_fundo = py5.color("#222")
celulas = 32
espacamento = 0
traco = 2
rotacoes = range(0, 360, 45)
camadas = 2
fundo = py5.color("#000")
borda = t.Borda(fundo, espacamento)


@dataclass
class CuboRotacao:
    x: float = -15
    y: float = 45
    z: float = 0
    dist_z: float = -500


rotacao = CuboRotacao()


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
    nomes_paletas = ["mandarin-redux", "pastel"]
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
    for idz in range(0, camadas):
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
    py5.window_title("Regenerando células...")
    largura, altura = helpers.DIMENSOES.internal
    colecao = gera_colecao(largura / celulas, altura / celulas)
    retorno = calcula_celulas(
        largura, altura, celulas, celulas, espacamento, espacamento, colecao, borda
    )
    py5.window_title("Células regeneradas")
    return retorno


def gera_imagem(
    celulas: list[tuple[t.Celula, tuple[t.Padrao, float, t.CoresPadrao, float]]],
):
    """Gera a imagem do sketch a partir das células calculadas.

    :param celulas: Lista de tuplas ``(celula, (padrao, rotacao, cores, z))``.
    """
    pg = py5.create_graphics(*helpers.DIMENSOES.internal, py5.P3D)
    with pg.begin_draw():
        pg.background(cor_fundo)
        for celula, (padrao, rotacao, cores, z) in celulas:
            celula(padrao, rotacao, cores, z=z, pg=pg)
    return pg


def setup():
    """Inicializa o sketch: cria a janela, calcula grade e padrões."""
    global imagem
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.background(cor_fundo)
    imagem = gera_imagem(inicializa_celulas())


def draw():
    """Renderiza todas as células e adiciona os créditos do sketch."""
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, rotacao.dist_z)
        forma = py5.create_shape(py5.BOX, 400)
        forma.rotate_y(py5.radians(rotacao.y))
        forma.rotate_x(py5.radians(rotacao.x))
        forma.rotate_z(py5.radians(rotacao.z))
        forma.set_texture(imagem)
        forma.set_stroke(True)
        forma.set_stroke(py5.color(0, 0, 0, 100))
        forma.set_stroke_weight(20)
        py5.shape(forma)
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
    global imagem
    key = py5.key
    key = py5.key
    match key:
        case " ":
            save_and_close()
        case "r":
            imagem = gera_imagem(inicializa_celulas())
        case "+":
            rotacao.dist_z += 100
        case "-":
            rotacao.dist_z -= 100
    match py5.key_code:
        case py5.UP:
            rotacao.x += 3
        case py5.DOWN:
            rotacao.x -= 3
        case py5.LEFT:
            rotacao.y += 3
        case py5.RIGHT:
            rotacao.y -= 3


def save_and_close():
    """Para o loop, salva a imagem do sketch e encerra."""
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
