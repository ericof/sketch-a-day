"""2026-07-18
(Não) Concêntricos 07
Exercício de criação de sketch baseado em formas geométricas concêntricas
ericof.com|https://ericof.com/en/sketches/2024-08-17
png
Sketch,py5,CreativeCoding
"""

from sketches.padroes.poligonos import gera_poligono_regular
from sketches.utils.draw import canvas
from sketches.utils.draw.cores import rgb_hex_to_hsb
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo_interna = py5.color(46, 12, 98)
cor_fundo = py5.color(0)


total_lados: int = 12
distribuicao: int = 3

ajuste_x: int = 0
ajuste_y: int = 400
tamanho_inicial: int = 1500
tamanho_final: int = 5
passo: int = -20
tamanhos = list(range(tamanho_inicial, tamanho_final, passo))
rotacao_inicial: int = 0
rotacao_passo: float = 0.3
traco: int = 6

total = len(tamanhos)
h, s, b = rgb_hex_to_hsb("#F137A6")


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.shape_mode(py5.CENTER)


def calcula_cores_traco(idx: int) -> tuple[int, int]:
    """Calcula cor de traço, cor de pintura e peso do traço de uma forma.

    :param idx: Índice da forma na sequência concêntrica.
    :param total: Total de formas, usado para atenuar o brilho da pintura.
    :returns: Tupla ``(cor_traco, cor_pintura)``, onde o peso
        do traço deriva de ``idx % 4``.
    """
    mult = 1 - (idx / total)
    if (idx % distribuicao) == 0:
        cor_traco = cor_pintura = cor_fundo_interna
    else:
        cor_traco = py5.color(h, s, 80)
        cor_pintura = py5.color(h, s, b * mult)
    return cor_traco, cor_pintura


def desenha_fundo():
    with py5.push():
        py5.rect_mode(py5.CORNER)
        py5.no_stroke()
        py5.fill(cor_fundo)
        x, y = 0, 0
        tamanho_x, tamanho_y = helpers.DIMENSOES.external
        py5.rect(x, y, tamanho_x, tamanho_y)


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, -1)
        desenha_fundo()
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, 0)
        rotacao = rotacao_inicial
        for idx, tamanho in enumerate(tamanhos):
            forma = gera_poligono_regular(
                lados=total_lados, largura=tamanho, altura=tamanho, rotacao=rotacao
            )
            rotacao += rotacao_passo
            cor_traco, cor_pintura = calcula_cores_traco(idx)
            if traco:
                forma.set_stroke_weight(traco)
                forma.set_stroke(cor_traco)
                forma.set_fill(False)
            else:
                forma.set_no_stroke()
                forma.set_fill(cor_pintura)
            py5.shape(forma, ajuste_x, ajuste_y, tamanho, tamanho)
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
