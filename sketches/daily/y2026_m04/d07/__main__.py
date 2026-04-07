"""2026-04-07
Language 10
Cubo com textura de grades compostas por padrões de traços e círculos. (Referência, filme Contato)
ericof.com
png
Sketch,py5,CreativeCoding
"""  # noQA: E501

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
camadas = 3
fundo = py5.color("#000")
borda = t.Borda(fundo, espacamento)
tamanho_cubo = 460
profundidade_face = 20


@dataclass
class CuboRotacao:
    x: float = -15
    y: float = 45
    z: float = 0
    dist_z: float = -500
    explosao: float = 60


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
    nomes_paletas = ["bright-colors"]
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


def cria_face(
    largura: float,
    altura: float,
    profundidade: float,
    textura,
) -> py5.Py5Shape:
    """Cria um slab paralelepípedo com a mesma textura em todas as faces.

    O slab é construído em coordenadas locais centrado na origem. A face
    externa fica em ``+Z`` local. Todas as 6 faces (externa, interna e as 4
    laterais) recebem a mesma textura mapeada com UV completo (0..1).

    :param largura: Lado da face externa no eixo X local.
    :param altura: Lado da face externa no eixo Y local.
    :param profundidade: Espessura do slab no eixo Z local.
    :param textura: Py5Graphics aplicado em todas as faces.
    :returns: Py5Shape com a textura aplicada às 6 faces.
    """
    w, h, d = largura / 2, altura / 2, profundidade / 2

    forma = py5.create_shape()
    with forma.begin_shape(py5.QUADS):
        forma.no_stroke()
        forma.texture_mode(py5.NORMAL)
        forma.texture(textura)
        # Externa (+Z local)
        forma.vertex(-w, -h, d, 0, 0)
        forma.vertex(w, -h, d, 1, 0)
        forma.vertex(w, h, d, 1, 1)
        forma.vertex(-w, h, d, 0, 1)
        # Interna (-Z local)
        forma.vertex(-w, -h, -d, 0, 0)
        forma.vertex(-w, h, -d, 0, 1)
        forma.vertex(w, h, -d, 1, 1)
        forma.vertex(w, -h, -d, 1, 0)
        # Lateral +X
        forma.vertex(w, -h, -d, 0, 0)
        forma.vertex(w, h, -d, 0, 1)
        forma.vertex(w, h, d, 1, 1)
        forma.vertex(w, -h, d, 1, 0)
        # Lateral -X
        forma.vertex(-w, -h, -d, 0, 0)
        forma.vertex(-w, -h, d, 1, 0)
        forma.vertex(-w, h, d, 1, 1)
        forma.vertex(-w, h, -d, 0, 1)
        # Lateral +Y
        forma.vertex(-w, h, -d, 0, 0)
        forma.vertex(-w, h, d, 0, 1)
        forma.vertex(w, h, d, 1, 1)
        forma.vertex(w, h, -d, 1, 0)
        # Lateral -Y
        forma.vertex(-w, -h, -d, 0, 0)
        forma.vertex(w, -h, -d, 1, 0)
        forma.vertex(w, -h, d, 1, 1)
        forma.vertex(-w, -h, d, 0, 1)

    return forma


def gera_faces(
    textura,
) -> list[tuple[py5.Py5Shape, tuple[float, float, float], tuple[float, float, float]]]:
    """Gera as 6 faces do cubo como slabs com textura nas 6 superfícies.

    Cada face compartilha o mesmo Py5Shape (e portanto a mesma textura). A
    explosão é aplicada no momento do desenho.

    :param textura: Py5Graphics aplicado como textura em todas as faces do slab.
    :returns: Lista ``[(shape, (tx, ty, tz), (rx, ry, rz)), ...]`` com seis
        entradas, uma por face do cubo.
    """
    forma = cria_face(
        tamanho_cubo,
        tamanho_cubo,
        profundidade_face,
        textura,
    )
    # O slab tem face externa em +Z local (z=+d). Para a face externa coincidir
    # com a superfície do cubo (em ±tamanho_cubo/2), o centro do slab fica a
    # tamanho_cubo/2 - profundidade_face/2 do centro do cubo.
    base = tamanho_cubo / 2 - profundidade_face / 2
    r90 = float(py5.radians(90))
    r180 = float(py5.radians(180))
    faces = [
        # +Z (frente) — orientação local já está alinhada
        (forma, (0, 0, base), (0, 0, 0)),
        # -Z (trás)
        (forma, (0, 0, -base), (0, r180, 0)),
        # +X (direita)
        (forma, (base, 0, 0), (0, r90, 0)),
        # -X (esquerda)
        (forma, (-base, 0, 0), (0, -r90, 0)),
        # +Y (base)
        (forma, (0, base, 0), (-r90, 0, 0)),
        # -Y (topo)
        (forma, (0, -base, 0), (r90, 0, 0)),
    ]
    return faces


def setup():
    """Inicializa o sketch: cria a janela, calcula grade e padrões."""
    global imagem, faces
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.background(cor_fundo)
    imagem = gera_imagem(inicializa_celulas())
    faces = gera_faces(imagem)


def draw():
    """Renderiza todas as células e adiciona os créditos do sketch."""
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, rotacao.dist_z)
        py5.rotate_y(float(py5.radians(rotacao.y)))
        py5.rotate_x(float(py5.radians(rotacao.x)))
        py5.rotate_z(float(py5.radians(rotacao.z)))
        # Fator de explosão: empurra cada face para fora do centro do cubo
        # ao longo do seu próprio eixo (a face já está orientada com +Z local
        # apontando para fora, então basta deslocar em +Z local).
        for forma, (tx, ty, tz), (rx, ry, rz) in faces:
            with py5.push():
                py5.translate(tx, ty, tz)
                if rx:
                    py5.rotate_x(rx)
                if ry:
                    py5.rotate_y(ry)
                if rz:
                    py5.rotate_z(rz)
                py5.translate(0, 0, rotacao.explosao)
                py5.shape(forma)
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def trata_tecla(key: str) -> None:
    """Trata teclas de caractere: salvar, regenerar, zoom e explosão."""
    global imagem, faces
    match key:
        case " ":
            save_and_close()
        case "r":
            imagem = gera_imagem(inicializa_celulas())
            faces = gera_faces(imagem)
        case "+":
            rotacao.dist_z += 100
        case "-":
            rotacao.dist_z -= 100
        case "]":
            rotacao.explosao += 10
        case "[":
            rotacao.explosao = max(0, rotacao.explosao - 10)


def key_pressed():
    """Captura teclas: ``espaço`` salva e fecha o sketch."""
    trata_tecla(py5.key)
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
