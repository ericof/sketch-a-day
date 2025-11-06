"""2025-11-06
Polígonos Redux 10
Exercício de criação de polígonos regulares com paleta de cores.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from sketches.padroes.poligonos import gera_poligono_regular
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

dimensoes = helpers.DIMENSOES
BUFFER: int = 800
LADOS: int = 6
LARG_MIN: int = dimensoes.internal[0] // 10
LARG_MAX: int = dimensoes.external[0]
PASSO: int = (LARG_MAX - LARG_MIN) // 30
TRACO: int = 12
TRACO_PASSO: float = 0.25

VERTICES = tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]


def cores_vertices(lados: int, paleta: deque) -> list[int]:
    """Gera uma lista de cores para os vértices de um polígono."""
    cores = []
    for _ in range(lados):
        cor = paleta[0]
        cores.append(cor)
        paleta.rotate(1)
    return cores


def setup():
    py5.size(*dimensoes.external, py5.P3D)


def posicoes(vertices: VERTICES) -> VERTICES:
    """Retorna as posições dos vértices."""
    resposta = []
    mult = [
        (1, 1),
        (-1, 1),
        (-1, -1),
        (1, -1),
    ]
    for idx, (x, y) in enumerate(vertices):
        mx, my = mult[idx]
        buffer_x = BUFFER * mx
        buffer_y = BUFFER * my
        x += buffer_x
        y += buffer_y
        resposta.append((x, y))

    return tuple(resposta)


def draw():
    cor_fundo = py5.color(0)
    py5.background(cor_fundo)
    py5.rect_mode(py5.CORNER)
    py5.shape_mode(py5.CENTER)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.blend_mode(py5.BLEND)
    vertices = posicoes(dimensoes.vertices_interno)
    paleta: deque[py5.Py5Color] = gera_paleta("Warhol", True)
    lados_base = LADOS
    for x, y in vertices:
        traco = TRACO
        with py5.push_matrix():
            py5.translate(x, y, -5)
            for d in range(LARG_MIN, LARG_MAX, PASSO):
                cores = cores_vertices(lados_base, paleta)
                forma = gera_poligono_regular(
                    lados=lados_base,
                    largura=d,
                    altura=d,
                    rotacao=np.pi / lados_base,
                )
                traco -= TRACO_PASSO
                forma.set_fill(False)
                forma.set_stroke_weight(traco)
                forma.set_strokes(cores)
                py5.shape(forma, 0, 0)

    # Credits and go
    canvas.sketch_frame(
        sketch, cor_fundo, "large_transparent_white", "transparent_white"
    )

    parametros = (
        f"Params: {LADOS} - {LARG_MIN} - {LARG_MAX} - {PASSO} - {TRACO} - {TRACO_PASSO}"
        f" - {BUFFER}"
    )
    py5.window_title(parametros)
    with py5.push():
        py5.translate(0, 0, 10)
        canvas.draw_text_box(
            parametros, style_name="transparent_white", x=20, y=950, align=py5.LEFT
        )


def key_pressed():  # noQA: C901
    global LADOS, LARG_MIN, LARG_MAX, PASSO, TRACO, TRACO_PASSO, BUFFER
    key = py5.key
    match key:
        case " ":
            save_and_close()
        case "+":
            LADOS += 1
        case "-":
            LADOS -= 1 if LADOS > 3 else 0
        case ">":
            LARG_MIN += 5
        case "<":
            LARG_MIN -= 5 if LARG_MIN > 10 else 0
        case "]":
            LARG_MAX += 5
        case "[":
            LARG_MAX -= 5 if LARG_MAX > LARG_MIN else 0
        case "w":
            PASSO += 1
        case "s":
            PASSO -= 1 if PASSO > 1 else 0
        case "a":
            TRACO += 1
        case "d":
            TRACO -= 1 if TRACO > 1 else 0
        case "t":
            TRACO_PASSO *= 1.1
        case "g":
            TRACO_PASSO *= 0.9
        case "z":
            BUFFER -= 5
        case "x":
            BUFFER += 5


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
