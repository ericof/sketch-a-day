"""2026-08-03
Grow a seed 01
Árvore com tronco marrom, folhas amareladas e flores vermelhas.
ericof.com|https://ericof.com/en/sketches/2024-01-26
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)


regras = {
    "X": "F++[![X]-X!][@X][--![XP]!]-F[-GFXP]+XP",
    "F": "FGF",
}
axioma = "X"
iteracoes = 6
max_angulo = 20
angulo = py5.radians(max_angulo)
tamanho = 4
escala = 0.5

# espessura do caule: começa em `tronco_inicial` e afina `tronco_decaimento`
# por segmento F até o piso `tronco_min`; salva/restaura por ramo (colchetes)
tronco_inicial = 8
tronco_min = 1
tronco_decaimento = 0.1
pilha_tronco = []

# ângulos de rotação (radianos) pré-computados para as pétalas de folha e flor
angulos_folha: tuple[float, ...] = tuple(
    float(py5.radians(idx)) for idx in range(30, 180, 60)
)
angulos_flor: tuple[float, ...] = tuple(
    float(py5.radians(idx)) for idx in range(0, 180, 60)
)

# cores
caule = "#452711"
flor = py5.color(200, 80, 0)
folha = py5.color(255, 200, 0)
no = py5.color(0, 255, 0)


def gera_frase() -> str:
    """Expande o axioma aplicando as regras de reescrita `iteracoes` vezes.

    :returns: a frase final da L-system após todas as iterações.
    """
    frase = axioma
    for _ in range(iteracoes):
        frase = "".join(regras.get(simbolo, simbolo) for simbolo in frase)
    return frase


def _s_caule():
    """Desenha um segmento de caule (F) e avança o tronco afinando-o."""
    global tronco
    py5.stroke_weight(tronco)
    py5.stroke(caule)
    py5.line(0, 0, 0, -tamanho)
    direcao = -1 if angulo > 0 else 1
    py5.bezier(
        0,
        0,
        -tamanho,
        (-tamanho / 4) * direcao,
        -tamanho,
        (-tamanho / 4) * direcao * 2,
        0,
        -tamanho,
    )
    py5.rotate_y(py5.HALF_PI / 18)
    if tronco > tronco_min:
        tronco -= tronco_decaimento


def _s_inverte_angulo():
    """Inverte o sinal do ângulo de ramificação (!)."""
    global angulo
    angulo = -angulo


def _s_ramo_abre():
    """Abre um ramo (`[`): empilha a matriz e a espessura atual do tronco."""
    pilha_tronco.append(tronco)
    py5.push_matrix()


def _s_ramo_fecha():
    """Fecha um ramo (`]`): restaura a matriz e a espessura do tronco."""
    global tronco
    py5.pop_matrix()
    tronco = pilha_tronco.pop()


def _s_no():
    """Desenha um nó de crescimento (@), aplicando a escala do ramo."""
    py5.scale(escala)
    py5.stroke_weight(tamanho)
    py5.stroke(no)
    py5.point(0, 0)


def _s_folha():
    """Desenha as pétalas de uma folha (X) em torno do ponto atual."""
    py5.stroke_weight(tamanho)
    py5.stroke(folha)
    with py5.push_matrix():
        for ang in angulos_folha:
            py5.rotate(ang)
            py5.point(0, +tamanho / 3)


def _s_flor():
    """Desenha as pétalas de uma flor (P) em torno do ponto atual."""
    py5.stroke_weight(tamanho)
    py5.stroke(flor)
    with py5.push_matrix():
        for ang in angulos_flor:
            py5.rotate(ang)
            py5.point(0, +tamanho / 2)


_ACOES = {
    "F": _s_caule,
    "G": lambda: py5.translate(0, -tamanho),
    "+": lambda: py5.rotate(-angulo),
    "-": lambda: py5.rotate(angulo),
    "!": _s_inverte_angulo,
    "[": _s_ramo_abre,
    "]": _s_ramo_fecha,
    "@": _s_no,
    "X": _s_folha,
    "P": _s_flor,
}


def desenha_frase():
    global tronco
    tronco = tronco_inicial
    pilha_tronco.clear()
    for simbolo in frase:
        acao = _ACOES.get(simbolo)
        if acao is not None:
            acao()


def setup():
    global frase
    py5.size(*helpers.DIMENSOES.external)
    frase = gera_frase()


def draw():
    py5.background(cor_fundo)
    with py5.push():
        with py5.push():
            py5.stroke(252, 249, 230)
            py5.fill(252, 249, 230)
            py5.rect(*helpers.DIMENSOES.pos_interno, *helpers.DIMENSOES.internal)
        x0 = helpers.DIMENSOES.centro[0]
        py5.translate(x0, 900)
        py5.rotate_y(py5.radians(py5.mouse_x))
        desenha_frase()
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
