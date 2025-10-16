"""2025-10-16
MSX Basic: Código de Barras 06
Desenho com barras simulando um código baseado em código MSX Basic.
ericof.com|https://github.com/gilbertfrancois/msx/blob/master/src/basic/barcode.bas
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

A = (py5.random() - 1) * 0.3
W = py5.random() * 1000
LARGURA = 800
ALTURA = 800
PASSO_Y = 25
PASSO_X = 4


def barras():
    paleta = gera_paleta("italia-01", True)
    metade_l = LARGURA // 2
    metade_a = ALTURA // 2
    for y0 in range(-metade_a, metade_a + 1, PASSO_Y):
        for x0 in range(-metade_l, metade_l + 1, PASSO_X):
            yv = (
                y0
                / metade_a
                * 18
                * py5.cos(py5.radians(-A + x0 / LARGURA * 9))
                * (py5.sin(py5.radians(y0 / metade_a * 7)))
            )
            y1 = y0 + yv + x0 * A
            py5.stroke(paleta[0])
            py5.point(x0, y1)
            PR = py5.random(10)
            c1 = paleta[1] if PR > 5.0 else paleta[0]
            py5.stroke(c1)
            py5.line(x0, y1 + 1, x0, metade_a)
        paleta.rotate()


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)


def draw():
    cor_fundo = py5.color(0)
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, -100)
        barras()
    parametros = f"Params: {LARGURA} - {ALTURA} - {PASSO_X} - {PASSO_Y}"
    py5.window_title(parametros)
    # Credits and go
    canvas.sketch_frame(
        sketch, cor_fundo, "large_transparent_white", "transparent_white"
    )
    with py5.push():
        py5.translate(0, 0, 10)
        canvas.draw_text_box(
            parametros, style_name="transparent_white", x=20, y=950, align=py5.LEFT
        )


def key_pressed():
    global LARGURA, ALTURA, PASSO_X, PASSO_Y
    key = py5.key
    match key:
        case " ":
            save_and_close()
        case "+":
            LARGURA += 5
        case "-":
            LARGURA -= 5 if LARGURA > 5 else 0
        case ">":
            ALTURA += 5
        case "<":
            ALTURA -= 5 if ALTURA > 2 else 0
        case "w":
            PASSO_Y += 1
        case "s":
            PASSO_Y -= 1 if PASSO_Y > 1 else 2
        case "d":
            PASSO_X += 2
        case "a":
            PASSO_X -= 1 if PASSO_X > 1 else 0


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
