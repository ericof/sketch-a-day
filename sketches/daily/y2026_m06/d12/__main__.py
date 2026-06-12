"""2026-06-12
My Valentine'Day
Parabéns a minha esposa, que celebra seu aniversário hoje.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
y_offset = 0


LIMITES = [650, 700, 725, 750, 750, 725, 700, 650]
forma: py5.Py5Shape | None = None


def calcula_pontos(lim_inferior: int, lim_superior: int) -> list[tuple[float, float]]:
    pontos = []
    for t in range(lim_inferior, lim_superior):
        x = 16 * (np.sin(t)) ** 3
        y = (
            (13 * np.cos(t))
            - (5 * np.cos(2 * t))
            - (2 * np.cos(3 * t))
            - (np.cos(4 * t))
        )
        pontos.append((x, -y))
    return pontos


def criar_forma(pontos: list[tuple[float, float]]) -> py5.Py5Shape:
    forma = py5.create_shape()
    with forma.begin_closed_shape():
        for x, y in pontos:
            forma.vertex(x, y)
    return forma


def setup():
    global forma
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.stroke_weight(2)
    py5.frame_rate(1)
    largura, _ = helpers.DIMENSOES.internal
    limite = largura // 2
    lim_inferior, lim_superior = -limite, limite
    pontos = calcula_pontos(lim_inferior, lim_superior)
    forma = criar_forma(pontos)


def draw():
    py5.background(cor_fundo)
    frame = py5.frame_count
    lista_indice = frame % 8 - 1 if frame % 8 else 7
    limite = LIMITES[lista_indice]
    if forma:
        with py5.push_matrix():
            x, yb = helpers.DIMENSOES.centro
            y = yb + y_offset
            py5.translate(x, y, -10)
            o = 10
            for idx in range(limite, 50, -25):
                color = py5.color(255, 0, 0, o)
                forma.set_stroke(color)
                forma.set_stroke_weight(1)
                forma.set_fill(color)
                py5.shape(forma, 0, 0, idx, idx)
                o += 10

    msg = f"y_offset: {y_offset} | lista_indice: {lista_indice} "
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
    global y_offset
    key = py5.key
    match key:
        case "+":
            y_offset += 10
        case "-":
            y_offset -= 10
        case " ":
            save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
