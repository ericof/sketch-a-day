"""2026-04-28
Vitral 05
Inspirado em vitrais, sketch com hexágonos e octágonos.
ericof.com|https://ericof.com/en/sketches/2023-06-01
png
Sketch,py5,CreativeCoding,Mosaico,Vitral
"""

from random import shuffle
from sketches.utils.draw import canvas
from sketches.utils.draw.formas import gera_hexagono
from sketches.utils.draw.formas import gera_octagono
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)


hexagono: py5.Py5Shape | None = None
octagono: py5.Py5Shape | None = None
tamanho = 40
h_diff = 40
pontos: list[tuple[float, float]] = []


def calcula_pontos() -> list[tuple[float, float]]:
    """Calcula a grade escalonada de pontos onde os hexágonos serão posicionados.

    Gera coordenadas em linhas alternadas (com deslocamento horizontal de meia
    célula em linhas ímpares) cobrindo as dimensões externas do canvas, e
    embaralha a ordem para que a renderização por índice produza variação
    cromática não-sequencial.

    :returns: lista de pares ``(x, y)`` com as posições dos hexágonos.
    """
    global pontos
    pontos = []
    for idy, y in enumerate(range(0, helpers.DIMENSOES.external[1], tamanho)):
        buffer_x = 0 if idy % 2 else tamanho // 2
        for x in range(0, helpers.DIMENSOES.external[0], tamanho):
            pontos.append((x + buffer_x, y))
    shuffle(pontos)
    return pontos


def cores_elemento(idx: int, angulo: float) -> tuple[int, int]:
    """Deriva as cores de traço e preenchimento de um hexágono.

    Distribui o matiz pelo ângulo dourado (≈137.508°) no índice,
    gerando uma sequência quase aleatória sem bandas visíveis.
    Saturação e brilho são modulados por módulos coprimos (41 e 20),
    variando em ``60..100`` e ``80..99`` respectivamente — a faixa
    estreita de brilho mantém a paleta sempre luminosa. O parâmetro
    ``angulo`` atua como offset adicional do matiz e modula a
    transparência; mesmo passado como valor fixo, deslocaria toda a
    paleta cromática. O traço permanece escuro, reforçando o efeito
    de vitral.

    :param idx: índice do ponto na grade embaralhada.
    :param angulo: ângulo, em graus, usado como offset do matiz e
        para modular a transparência do preenchimento.
    :returns: par ``(traco, cor)`` com os valores ``py5.color`` para
        stroke e fill.
    """
    h = (idx * 137.508 + h_diff + angulo * 0.7) % 360
    s = 60 + (idx % 41)
    b = 80 + ((idx * 7) % 20)
    t = angulo / 6 + 60
    traco = py5.color(h, 30, 0)
    cor = py5.color(h, s, b, t)
    return traco, cor


def setup():
    """Inicializa o sketch.

    Define o tamanho do canvas, ativa P3D e o modo de cor HSB, cria o
    hexágono-base e calcula a grade de posicionamento.
    """
    global hexagono, octagono
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.shape_mode(py5.CENTER)
    py5.color_mode(py5.HSB, 360, 100, 100)
    hexagono = gera_hexagono()
    octagono = gera_octagono()
    calcula_pontos()


def draw():
    """Desenha o quadro atual.

    Percorre a grade de pontos uma única vez, aplicando ao hexágono as
    cores devolvidas por :func:`cores_elemento` (chamada com
    ``angulo=90`` fixo). O traço alterna por paridade do índice —
    hexágonos pares ficam sem stroke, ímpares recebem traço escuro — e
    cada hexágono é desenhado com escala interna ``tamanho * 1.4`` para
    gerar sobreposição. Ao final, renderiza a moldura de créditos do
    sketch.
    """
    py5.background(cor_fundo)
    if hexagono and octagono:
        with py5.push():
            py5.translate(0, 0, -20)
            for idx, (x, y) in enumerate(pontos):
                traco, cor = cores_elemento(idx, 90)
                forma = hexagono if idx % 2 else octagono
                if idx % 2:
                    forma.set_stroke(traco)
                    forma.set_stroke_weight(2)
                else:
                    forma.set_stroke(False)
                forma.set_fill(cor)
                tamanho_interno = tamanho * 1.4
                py5.shape(forma, x, y, tamanho_interno, tamanho_interno)
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
    - ``r``: recalcula (reembaralha) a grade de pontos.
    - ``+`` / ``-``: incrementa ou decrementa o tamanho do hexágono em 2px
      e recalcula a grade.
    - ``>`` / ``<``: incrementa ou decrementa a diferença de matiz em 2 unidades
      e recalcula a grade.
    """
    global tamanho, h_diff
    key = py5.key
    match key:
        case " ":
            save_and_close()
        case "r":
            calcula_pontos()
        case "+":
            tamanho += 2
            calcula_pontos()
        case "-":
            tamanho -= 2
            calcula_pontos()
        case ">":
            h_diff += 2
            calcula_pontos()
        case "<":
            h_diff -= 2
            calcula_pontos()


def save_and_close():
    """Pausa o loop, salva o PNG do sketch e encerra a execução."""
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
