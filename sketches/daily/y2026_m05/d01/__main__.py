"""2026-05-01
Vitral 08
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
tamanho = 40
h_diff = 40
grade: list[tuple[int, float, int, float]] | None = None
celula_x = 0
celula_y = 0
celulas = 1
banda = 10


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

    Combina os índices de coluna (``idx``) e linha (``idy``) com pesos
    coprimos antes de aplicar passo quasi-dourado no matiz (``122.508``
    por unidade), produzindo distribuição 2D quasi-aleatória sem
    bandas horizontais nem verticais perceptíveis. O matiz percorre
    todo o círculo cromático; a saturação varia em ``80..100`` (módulo
    21), mantendo a paleta sempre vibrante. Já o brilho **não é mais
    quasi-aleatório**: vale ``100 - (|cx - idx| + |cy - idy|)`` com
    ``cx = cy = celulas // 2``, criando uma vinheta em distância de
    Manhattan que escurece os elementos conforme se afastam do centro
    da grade. O ``angulo`` atua como offset adicional do matiz e
    modula a transparência (``t = angulo / 6 + 70``); o traço
    permanece escuro, reforçando o efeito de vitral.

    :param idx: índice da coluna na grade.
    :param idy: índice da linha na grade.
    :param angulo: ângulo, em graus, usado como offset do matiz e
        para modular a transparência do preenchimento.
    :returns: par ``(traco, cor)`` com os valores ``py5.color`` para
        stroke e fill.
    """
    h = ((idx + idy * 34) * 122.508 + h_diff + angulo * 0.8) % 360
    s = 80 + ((idx + idy * 11) % 21)
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
    """Desenha o quadro atual com duas camadas rotacionadas.

    A uma profundidade ``z=-20``, empilha duas camadas rotacionadas em
    torno do eixo Y (0° e 45°). Em cada camada, percorre toda a grade
    escolhendo hexágono ou octágono pela regra ``(idx + idy) % 4 == 0``
    (um hexágono a cada quatro células). As cores vêm de
    :func:`cores_elemento` recebendo o ``angulo`` da camada — o que
    desloca matiz e transparência entre as duas — e cada forma é
    desenhada em escala ``celula * 1.4`` com stroke weight 8, gerando o
    contorno espesso típico de vitral.

    Ao final, renderiza a moldura de créditos do sketch.
    """
    py5.background(cor_fundo)
    if grade and hexagono and octagono:
        with py5.push():
            py5.translate(0, 0, -20)
            for angulo in range(0, 90, 45):
                with py5.push():
                    py5.rotate_y(py5.radians(angulo))
                    for idx, x, idy, y in grade:
                        traco, cor = cores_elemento(idx, idy, angulo)
                        forma = hexagono if (idx + idy) % 4 == 0 else octagono
                        forma.set_stroke(traco)
                        forma.set_stroke_weight(8)
                        forma.set_fill(cor)
                        mult = 1.4
                        py5.shape(forma, x, y, celula_x * mult, celula_y * mult)
    msg = f"T: {tamanho}, H: {h_diff}"
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
    - ``>`` / ``<``: incrementa ou decrementa ``h_diff`` (offset de
      matiz aplicado em :func:`cores_elemento`) em 2 unidades e
      recalcula a grade.
    """
    global tamanho, h_diff
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
            h_diff += 2
            calcula_grade()
        case "<":
            h_diff -= 2
            calcula_grade()


def save_and_close():
    """Pausa o loop, salva o PNG do sketch e encerra a execução."""
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
