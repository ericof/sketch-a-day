"""2026-07-06
Recursive Squares 04
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

areas = [
    (200, 200, 395, gera_paleta("laranja")),
    (600, 600, 395, gera_paleta("laranja")),
    (200, 600, 395, gera_paleta("laranja")),
    (600, 200, 395, gera_paleta("laranja")),
]

cor_fundo = py5.color(0)
z_base = -28
z_divisor = 2
z_passo = 8

traco = 3


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
    z = -40
    for ida, angulo in enumerate(range(0, 75, 3)):
        tamanho = tamanho_base * (1 - (angulo / 70)) if ida else tamanho_base
        cor = paleta[0]
        paleta.rotate()
        z = z_base + ((ida // z_divisor) * z_passo)
        with py5.push():
            py5.translate(cx, cy, z)
            if reflete_v:
                py5.scale(1, -1)
            py5.rotate(py5.radians(reflete_h * angulo))
            py5.stroke(cor)
            py5.square(0, 0, tamanho)


def draw() -> None:
    py5.background(cor_fundo)
    py5.no_fill()
    py5.stroke_weight(traco)

    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, -420)
        py5.rotate_x(py5.radians(45))
        for cx, cy, tamanho_base, paleta in areas:
            paleta_deque: deque[int] = deque(paleta)
            desenha_quadrados(cx, cy, tamanho_base, paleta_deque)

    msg = (
        f"z_base: {z_base} | z_divisor: {z_divisor} | "
        f"z_passo: {z_passo} | traco: {traco}"
    )
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
    global z_base, z_divisor, z_passo, traco
    key = py5.key
    match key:
        case "w" | "s":
            z_base += 2 if key == "w" else -2
        case "a" | "d":
            z_passo += 1 if key == "d" else -1
        case ">" | "<":
            z_divisor += 1 if key == ">" else -1
        case "+" | "-":
            traco += 1 if key == "+" else -1
        case " ":
            save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
