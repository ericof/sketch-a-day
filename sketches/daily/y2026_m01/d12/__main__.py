"""2026-01-12
Padrão de Curvas Dinâmicas 05
Curvas que reagem à posição do mouse, criando um padrão fluído e em movimento.
ericof.com|https://openprocessing.org/sketch/2699138
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

num: float = 4.0
tnum: float = 26.0
mult: float = 1.0
start: float = 0.0
stretch: float = 5.0
lm: py5.Py5Vector = py5.Py5Vector(0, 0)


def setup():
    global lm
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.background("ivory")
    py5.no_cursor()


def desenha_padroes(largura, altura, paleta, target_x: float = 0, target_y: float = 0):
    global num, tnum, mult, start, stretch, lm
    target = py5.Py5Vector(target_x, target_y)
    lm = lm.lerp(target, 0.1)
    target_stretch = py5.floor(py5.remap(py5.mouse_y, 0, py5.height, 0.2, 6))
    stretch = py5.lerp(stretch, target_stretch, 0.1)
    num = py5.lerp(num, tnum, 0.1)
    mult = py5.lerp(mult, py5.remap(py5.mouse_x, 0, py5.width, 1, 4), 0.1)
    start = py5.lerp(start, py5.remap(py5.mouse_y, 0, py5.width, -12, 12), 0.1)
    # translucent fade
    py5.no_stroke()
    py5.fill(255, 255, 240, int(0.25 * 255))
    py5.rect(0, 0, py5.width, py5.height)

    # mouse marker
    # py5.fill(0, 20)
    # py5.ellipse(lm.x, lm.y, 20, 20)
    with py5.push():
        cor = paleta[0]
        paleta.rotate(1)
        py5.translate(largura / 2, altura / 2)
        py5.scale(0.95)
        py5.stroke(cor)
        py5.no_fill()
        py5.stroke_weight(2.1 * altura / 628)
        n = int(num)
        for i in range(n):
            a = py5.PI + i * py5.TAU / n

            # first pair (mirrored with scale(-1, 1))
            with py5.push():
                py5.rotate(a)
                cor = paleta[0]
                paleta.rotate(1)
                py5.stroke(cor)
                py5.curve(
                    -start * altura / 6,
                    -altura * stretch,
                    0,
                    altura / 48,
                    0,
                    altura / 2,
                    start * 3 * altura / 9,
                    3 * altura / 2,
                )
                py5.scale(-1, 1)
                py5.curve(
                    -start * altura / 6,
                    -altura * stretch,
                    0,
                    altura / 48,
                    0,
                    altura / 2,
                    start * 3 * altura / 9,
                    3 * altura / 2,
                )

            # second pair (scaled by mult and -mult)
            with py5.push():
                py5.rotate(a)

                with py5.push():
                    cor = paleta[0]
                    paleta.rotate(1)
                    py5.stroke(cor)
                    py5.scale(mult, 1)
                    py5.curve(
                        -start * altura / 6,
                        -altura * stretch,
                        0,
                        altura / 48,
                        0,
                        altura / 2,
                        start * 3 * altura / 9,
                        3 * altura / 2,
                    )

                with py5.push():
                    cor = paleta[0]
                    paleta.rotate(1)
                    py5.stroke(cor)
                    py5.scale(-mult, 1)
                    py5.curve(
                        -start * altura / 6,
                        -altura * stretch,
                        0,
                        altura / 48,
                        0,
                        altura / 2,
                        start * 3 * altura / 9,
                        3 * altura / 2,
                    )


def draw():
    py5.background("ivory")
    passo = 200
    areas = [
        (0, 0, gera_paleta("Warhol", True)),
        (0, 200, gera_paleta("pastel", True)),
        (0, 400, gera_paleta("bege-01", True)),
        (0, 600, gera_paleta("tons-azul-01", True)),
        (200, 0, gera_paleta("Warhol", True)),
        (200, 200, gera_paleta("pastel", True)),
        (200, 400, gera_paleta("pycon-colombia-2025", True)),
        (200, 600, gera_paleta("sunset-ocean", True)),
        (400, 0, gera_paleta("laranja-01", True)),
        (400, 200, gera_paleta("brasil-03", True)),
        (400, 400, gera_paleta("bege-02", True)),
        (400, 600, gera_paleta("bright-colors", True)),
        (600, 0, gera_paleta("mondrian", True)),
        (600, 200, gera_paleta("laranja-01", True)),
        (600, 400, gera_paleta("DJ1", True)),
        (600, 600, gera_paleta("Navy-Orange", True)),
    ]
    for idx, (ix, iy, paleta) in enumerate(areas):
        xb, yb = helpers.DIMENSOES.pos_interno
        x, y = xb + ix, yb + iy
        largura, altura = passo, passo
        with py5.push():
            py5.translate(x, y, -10)
            target_x, target_y = py5.mouse_x, py5.mouse_y
            target_x, target_y = target_x + idx, target_y + idx * 8
            desenha_padroes(largura, altura, paleta, target_x, target_y)

    py5.window_title(
        f"Mouse: {int(lm.x), int(lm.y)} "
        f"Num: {num:.2f} "
        f"Mult: {mult:.2f} "
        f"Stretch: {stretch:.2f}"
    )
    # Credits and go
    cor_fundo = py5.color(0)
    canvas.sketch_frame(
        sketch, cor_fundo, "large_transparent_white", "transparent_white"
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
