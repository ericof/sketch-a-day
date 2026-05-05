"""2026-05-05
Vitral 11
Inspirado em vitrais, sketch com hexágonos e octágonos.
ericof.com|https://ericof.com/en/sketches/2023-06-01
png
Sketch,py5,CreativeCoding,Mosaico,Vitral
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.formas import gera_hexagono
from sketches.utils.draw.formas import gera_octagono
from sketches.utils.draw.grade import cria_grade_ex
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)


hexagono: py5.Py5Shape | None = None
octagono: py5.Py5Shape | None = None
tamanho = 30
h_base = 40
h_jitter = 15
grade: list[tuple[int, float, int, float]] | None = None
celula_x = 0
celula_y = 0
celulas = 1
banda = 20


def pos(pos: float) -> float:
    """Aplica jitter aleatório uniforme a uma coordenada.

    Soma um inteiro sorteado em ``[-banda, banda]`` à coordenada
    recebida, quebrando o alinhamento perfeito da grade e dando um ar
    artesanal — como peças de vitral cortadas à mão — ao mosaico.

    :param pos: coordenada original (``x`` ou ``y``) em pixels.
    :returns: coordenada deslocada em até ``±banda`` pixels.
    """
    return pos + py5.random_int(-banda, banda)


def calcula_grade() -> list[tuple[int, float, int, float]]:
    """Calcula a grade escalonada de células para posicionar os elementos.

    Sorteia novas dimensões de célula (``celula_x`` e ``celula_y``) num
    intervalo entre ``1.2x`` e ``1.5x`` ``tamanho``, atualiza
    ``celulas`` (número aproximado de colunas, usado no cálculo do
    brilho radial em :func:`cores_elemento`) e gera a grade alternada
    via :func:`cria_grade_ex`. Em seguida aplica :func:`pos` a cada
    coordenada, introduzindo jitter de ``±banda`` pixels para suavizar
    o alinhamento. Cada item devolvido é a tupla ``(idx, x, idy, y)``
    com índices e coordenadas já deslocadas.

    :returns: lista de tuplas ``(idx, x, idy, y)``.
    """
    global grade, celula_x, celula_y, celulas
    celula_x = int(tamanho * py5.random(1.2, 1.5))
    celula_y = int(tamanho * py5.random(1.2, 1.5))
    celulas = helpers.DIMENSOES.external[0] // celula_x + 1
    grade = cria_grade_ex(
        largura=helpers.DIMENSOES.external[0],
        altura=helpers.DIMENSOES.external[1],
        margem_x=0,
        margem_y=0,
        celula_x=celula_x,
        celula_y=celula_y,
        alternada=True,
    )
    grade = [(idx, pos(x), idy, pos(y)) for idx, x, idy, y in grade]
    return grade


def cores_elemento(idx: int, idy: int, angulo: float) -> tuple[int, int]:
    """Deriva as cores de traço e preenchimento de um elemento da grade.

    A paleta é **analógica em torno de** ``h_base``: combina os
    índices de coluna (``idx``) e linha (``idy``) com pesos coprimos e
    aplica passo quasi-dourado (``122.508`` por unidade) para gerar
    uma distribuição 2D quasi-aleatória, mas em vez de cobrir todo o
    círculo cromático o resultado é mapeado para
    ``[-h_jitter, +h_jitter]`` e somado a ``h_base``, mantendo todas
    as peças como variações de uma mesma cor. O ``angulo`` adiciona
    um pequeno deslocamento extra de matiz (``angulo · 0.2``), o
    suficiente para diferenciar as duas camadas rotacionadas sem sair
    da família cromática.

    Para compensar a faixa estreita de matiz, a saturação foi
    alargada para ``60..100`` via ``(idx + idy · 11) % 41``,
    distribuindo quasi-aleatoriamente peças mais saturadas e mais
    "lavadas" pela grade (sem padrão espacial). O brilho mantém
    a vinheta em distância de Manhattan
    (``100 - (|cx - idx| + |cy - idy|)``, com ``cx = cy = celulas // 2``),
    escurecendo os elementos longe do centro. A transparência é
    modulada por ``t = angulo / 6 + 70`` e o traço permanece escuro
    (``saturação 30``, ``brilho 0``), reforçando o efeito de vitral.

    :param idx: índice da coluna na grade.
    :param idy: índice da linha na grade.
    :param angulo: ângulo, em graus, usado como offset adicional do
        matiz e para modular a transparência do preenchimento.
    :returns: par ``(traco, cor)`` com os valores ``py5.color`` para
        stroke e fill.
    """
    delta_h = ((idx + idy * 34) * 122.508) % (2 * h_jitter) - h_jitter
    h = (h_base + delta_h + angulo * 0.2) % 360
    s = 60 + ((idx + idy * 11) % 41)
    b = 100 - (abs(celulas // 2 - idx) + abs(celulas // 2 - idy))
    t = angulo / 6 + 70
    traco = py5.color(h, 30, 0)
    cor = py5.color(h, s, b, t)
    return traco, cor


def setup():
    """Inicializa o sketch.

    Define o tamanho do canvas, ativa P3D e o modo de cor HSB, cria os
    shapes-base (hexágono e octágono) e calcula a grade inicial.
    """
    global hexagono, octagono
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.shape_mode(py5.CENTER)
    py5.color_mode(py5.HSB, 360, 100, 100)
    hexagono = gera_hexagono()
    octagono = gera_octagono()
    calcula_grade()


def draw():
    """Desenha o quadro atual com três camadas rotacionadas.

    A uma profundidade ``z=-20``, empilha **três** camadas rotacionadas
    em torno do eixo Y (``0°``, ``30°`` e ``60°``). Em cada camada,
    percorre toda a grade escolhendo a forma pela regra
    ``(idx + idy) % 4 == 0``: as células marcadas recebem **hexágono**
    em escala generosa ``celula · 2.1`` com traço quase invisível
    (``stroke weight 1``); as demais recebem **octágono** em escala
    ``celula · 1.5`` com traço espesso (``stroke weight 8``). O
    contraste é extremo — hexágonos grandes e quase sem chumbo,
    octágonos médios com contorno pesado — criando um efeito de
    vitral em que as peças hexagonais "vazam" sobre as octogonais. As
    cores vêm de :func:`cores_elemento` recebendo o ``angulo`` da
    camada, deslocando matiz e transparência entre as três.

    Ao final, renderiza a moldura de créditos do sketch.
    """
    py5.background(cor_fundo)
    if grade and hexagono and octagono:
        with py5.push():
            py5.translate(0, 0, -20)
            for angulo in range(0, 90, 30):
                with py5.push():
                    py5.rotate_y(py5.radians(angulo))
                    for idx, x, idy, y in grade:
                        traco, cor = cores_elemento(idx, idy, angulo)
                        if (idx + idy) % 4 == 0:
                            forma = hexagono
                            mult = 2.1
                            traco_peso = 1
                        else:
                            forma = octagono
                            mult = 1.5
                            traco_peso = 8
                        forma.set_stroke(traco)
                        forma.set_stroke_weight(traco_peso)
                        forma.set_fill(cor)
                        py5.shape(forma, x, y, celula_x * mult, celula_y * mult)
    msg = f"T: {tamanho}, H: {h_base}"
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
        msg=msg,
    )


def key_pressed():
    """Trata atalhos de teclado.

    - ``space``: salva a imagem e encerra o sketch.
    - ``r``: recalcula a grade (sorteia novas dimensões de célula).
    - ``+`` / ``-``: incrementa ou decrementa ``tamanho`` (base usada
      para o sorteio das células) em 2px e recalcula a grade.
    - ``>`` / ``<``: incrementa ou decrementa ``h_base`` (matiz central
      da paleta analógica em :func:`cores_elemento`) em 10 graus e
      recalcula a grade.
    """
    global tamanho, h_base
    key = py5.key
    match key:
        case " ":
            save_and_close()
        case "r":
            calcula_grade()
        case "+":
            tamanho += 2
            calcula_grade()
        case "-":
            tamanho -= 2
            calcula_grade()
        case ">":
            h_base = (h_base + 10) % 360
            calcula_grade()
        case "<":
            h_base = (h_base - 10) % 360
            calcula_grade()


def save_and_close():
    """Pausa o loop, salva o PNG do sketch e encerra a execução."""
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
