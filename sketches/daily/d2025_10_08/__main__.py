"""2025-10-08
MSX Basic: Flor Mutante 12
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

PETALAS: int = 11
INTERACOES: int = 12
ROTACAO: bool = True
TRACO: int = 0
MULT: int = 40
N1: float = 7.0
N2: float = 2.0
PINTAR: bool = True


def desenha_flor(
    petalas: int,
    iteracoes: int = 10,
    rotacao: bool = False,
    traco: int = 5,
    mult: int = 4,
    n1: float = 5,
    n2: float = 4,
    pintar: bool = False,
):
    paleta = gera_paleta("Navy-Orange", True)
    buffer_x = 0
    buffer_y = 0
    centro_y = 0
    pi = py5.PI
    tau = py5.TAU
    with py5.push():
        for v in range(iteracoes, 0, -1):
            i = (v * pi / 30) * (1 if rotacao else 0)
            m1 = n1 * v
            m2 = n2 * v
            f = 0
            forma = py5.create_shape()
            cor = paleta[0]
            with forma.begin_closed_shape():
                forma.color_mode(py5.RGB)
                forma.stroke_weight(traco)
                forma.stroke(cor)
                forma.fill(cor) if pintar else forma.no_fill()
                while f < tau:
                    a = f - i
                    s = abs(py5.sin(f * petalas / 2))
                    r = s * m1 + m2
                    x = py5.cos(a) * r
                    y = py5.sin(a) * r
                    xp = x * mult + buffer_x
                    yp = buffer_y - (y * mult + centro_y)
                    forma.vertex(xp, yp)
                    f += tau / 180
            forma.set_name(f"flor-{v:03d}")
            py5.shape(forma)
            paleta.rotate()


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)


def draw():
    cor_fundo = py5.color(0)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    with py5.push():
        cx, cy = helpers.DIMENSOES.centro
        py5.translate(cx - 150, cy + 80, -20)
        desenha_flor(PETALAS, INTERACOES, ROTACAO, TRACO, MULT, N1, N2, PINTAR)
    parametros = (
        f"Params: {PETALAS} - {INTERACOES} - {ROTACAO} - {TRACO} - {MULT} - {N1} - {N2}"
        f" - {'Pintar' if PINTAR else 'Contorno'}"
    )
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


def key_pressed():  # noQA: C901
    global PETALAS, PINTAR, INTERACOES, ROTACAO, TRACO, MULT, N1, N2
    key = py5.key
    match key:
        case " ":
            save_and_close()
        case "+":
            INTERACOES += 1
        case "-":
            INTERACOES -= 1
        case "w":
            N1 += 1
        case "s":
            N1 -= 1
        case "a":
            N2 -= 1
        case "d":
            N2 += 1
        case "t":
            TRACO += 1
        case "g":
            TRACO -= 1 if TRACO > 0 else 0
        case "r":
            ROTACAO = not ROTACAO
        case ">":
            MULT += 1
        case "<":
            MULT -= 1
        case "]":
            PETALAS += 1
        case "[":
            PETALAS -= 1 if PETALAS > 3 else 0
        case "p":
            PINTAR = not PINTAR


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
