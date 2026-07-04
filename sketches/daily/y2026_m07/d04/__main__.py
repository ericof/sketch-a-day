"""2026-07-04
Recursive Squares 02
Desenha quadrados recursivamente
ericof.com
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

AREAS = [
    (200, 200, 395, gera_paleta("laranja", True)),
    (600, 600, 395, gera_paleta("laranja", True)),
    (200, 600, 395, gera_paleta("laranja", True)),
    (600, 200, 395, gera_paleta("laranja", True)),
]


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CENTER)


def desenha_quadrados(cx: float, cy: float, tamanho_base: float, paleta: deque[int]):
    # Espelhamento pela POSICAO no painel (nao por idx): areas a direita do
    # centro giram no sentido oposto (reflexo horizontal) e areas abaixo do
    # centro sao refletidas verticalmente via scale(1, -1). Chavear por posicao
    # evita o bug de ``idx // 2`` agrupar pela diagonal e misturar as linhas de
    # cima e de baixo. O tamanho usa a magnitude do angulo (loop 0->70), entao
    # espelho e reflexo so mudam a orientacao -- o tamanho aparente fica identico.
    centro_x = helpers.DIMENSOES.internal[0] / 2
    centro_y = helpers.DIMENSOES.internal[1] / 2
    reflete_h = 1 if cx < centro_x else -1
    reflete_v = cy > centro_y
    for ida, angulo in enumerate(range(0, 75, 3)):
        tamanho = tamanho_base * (1 - (angulo / 70)) if ida else tamanho_base
        cor = paleta[0]
        paleta.rotate()
        with py5.push():
            py5.translate(cx, cy, -10)
            if reflete_v:
                py5.scale(1, -1)
            py5.rotate(py5.radians(reflete_h * angulo))
            py5.stroke(cor)
            py5.square(0, 0, tamanho)


def draw():
    py5.background(cor_fundo)
    py5.no_fill()
    py5.stroke_weight(2)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, -10)
        for cx, cy, tamanho_base, paleta in AREAS:
            desenha_quadrados(cx, cy, tamanho_base, paleta)

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
