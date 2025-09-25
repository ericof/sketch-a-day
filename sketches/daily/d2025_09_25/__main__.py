"""2025-09-25
MSX Basic: Flor 04
Desenho de flor baseado em código MSX Basic.
ericof.com|https://marmsx.msxall.com/cursos/basic/basic_e7.html
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

paleta = gera_paleta("Warhol", True)


def desenha_flor(
    petalas: int,
    iteracoes: int = 10,
    rotacao: bool = False,
    traco: int = 5,
    mult: int = 4,
    n1: int = 5,
    n2: int = 4,
):
    buffer_x = 0
    buffer_y = 0
    centro_y = 0
    pi = py5.PI
    tau = py5.TAU
    py5.stroke_weight(traco)
    with py5.push():
        for v in range(0, iteracoes):
            i = (v * pi / 30) * (1 if rotacao else 0)
            m1 = n1 * v
            m2 = n2 * v
            f = 0
            x0 = None
            y0 = None
            py5.stroke(paleta[0])
            while f < tau:
                a = f - i
                s = abs(py5.sin(f * petalas / 2))
                r = s * m1 + m2
                x = py5.cos(a) * r
                y = py5.sin(a) * r
                xp = x * mult + buffer_x
                yp = buffer_y - (y * mult + centro_y)
                x0 = xp if f == 0 else x0
                y0 = yp if f == 0 else y0
                if f > 0:
                    py5.line(x0, y0, xp, yp)
                    x0 = xp
                    y0 = yp
                f += tau / 180
            paleta.rotate()


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color(0)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro)
        desenha_flor(5, 30, False, 6, 3, 8, 2)
    # Credits and go
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
