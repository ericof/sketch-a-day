"""2026-04-23
Petals 03
Círculos concêntricos, em azul
ericof.com | https://x.com/abakcus/status/2045535320809099361
png
Sketch,py5,CreativeCoding
"""

from collections.abc import Sequence
from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
cor_fundo_interna = py5.color(255)
z_interna = -10

extensao_min: int = 100
extensao_max: int = 700
passos_total: int = 6
cor_oceano: int = py5.color("#00B2D0", 50)


def calcula_ext_pos(
    largura: int,
    extensao_min: int = extensao_min,
    extensao_max: int = extensao_max,
    total: int = passos_total,
    reverso: bool = False,
) -> Sequence[tuple[float, float]]:
    """Calcula pares ``(x, extensao)`` para uma sequência de círculos crescentes.

    :param largura: Largura disponível, em pixels.
    :param extensao_min: Diâmetro do menor círculo da sequência.
    :param extensao_max: Diâmetro do maior círculo da sequência.
    :param total: Número de passos entre o menor e o maior círculo.
    :param reverso: Se ``True``, espelha a sequência a partir da borda direita.
    :returns: Pares ``(x, extensao)`` para cada círculo.
    """
    passo = (extensao_max - extensao_min) / total
    x0 = (largura - extensao_max) / 2 - (extensao_min / 2)
    if reverso:
        x0 = largura - x0
    pares = []
    extensao: float = extensao_min
    x = x0 + extensao
    while extensao <= extensao_max:
        raio = extensao / 2
        x_diff = -raio - extensao_min if reverso else raio + extensao_min
        pares.append((x, extensao))
        extensao += passo
        x = x0 + x_diff
    return pares


def desenha_fundo(extensao: int = extensao_max):
    """Desenha o disco branco de fundo interno, atrás das camadas de círculos.

    :param extensao: Diâmetro do disco de fundo.
    """
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, z_interna - 1)
        py5.ellipse_mode(py5.CENTER)
        py5.no_stroke()


def desenha_circulos(pares: Sequence[tuple[float, float]], cor: int, direcao: int = 1):
    """Desenha uma camada de meio-círculos sobre a área interna do sketch.

    :param pares: Pares ``(x, extensao)`` produzidos por :func:`calcula_ext_pos`.
    :param cor: Cor de preenchimento; o stroke é derivado com alpha reduzido.
    :param direcao: ``1`` para a metade superior, ``-1`` para a metade inferior.
    """
    with py5.push():
        traco = py5.color(
            py5.red(cor), py5.green(cor), py5.blue(cor), py5.alpha(cor) * 0.5
        )
        py5.fill(cor)
        py5.stroke(traco)
        py5.stroke_weight(2)
        _, centro_y = helpers.DIMENSOES.centro
        py5.translate(helpers.DIMENSOES.pos_interno[0], centro_y, z_interna)
        for x, extensao in pares:
            py5.circle(x, 0, extensao)


def setup():
    """Inicializa o canvas P3D e pré-calcula as sequências de pares (x, extensao)."""
    global pares, pares_reverso
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.RGB)
    passos = 6
    pares = calcula_ext_pos(helpers.DIMENSOES.internal[0], total=passos)
    pares_reverso = calcula_ext_pos(
        helpers.DIMENSOES.internal[0], total=passos, reverso=True
    )


def draw():
    """Loop principal: compõe céu, oceano e aplica a moldura de créditos."""
    py5.background(cor_fundo)
    desenha_fundo()
    desenha_circulos(pares, cor_oceano, -1)
    desenha_circulos(pares_reverso, cor_oceano, -1)
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def key_pressed():
    """Salva e encerra o sketch ao pressionar a barra de espaço."""
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    """Para o loop, grava o PNG final e encerra o sketch."""
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
