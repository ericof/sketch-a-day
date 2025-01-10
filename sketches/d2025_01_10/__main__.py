"""2025-01-10
TAU, TAU, TAU, TAU
Criação de padrão utilizando apenas TAU
png
Sketch,py5,CreativeCoding,genuary,genuary2025,genuary10
"""

from collections import deque

import opensimplex
import py5

from utils import helpers
from utils.draw import pontos_circulo

sketch = helpers.info_for_sketch(__file__, __doc__)

FUNDO = "#F8F6E3"
PALETA = deque(
    [
        "#97E7E1",
        "#6AD4DD",
        "#7AA2E3",
        "#074799",
        "#009990",
        "#E1FFBB",
    ]
)

gerador = opensimplex.seed(39874)

T = py5.TAU
T__ = (
    T * abs(py5.cos(T * T))
    + abs(py5.cos(T * T))
    + abs(py5.cos(T * T))
    + abs(py5.cos(T * T))
)


def cria_forma(raio_base: float, largura: float):
    total_pontos = int(T * T * T * T)
    vertices = []
    for idx in (1, -1):
        raio = raio_base + (idx * (largura / T__))
        pontos = []
        for xb, yb in pontos_circulo(total_pontos, raio):
            ruido = opensimplex.noise2(xb, yb)
            x = xb + (ruido * T)
            y = yb + (ruido * T)
            pontos.append((x, y))
        vertices.append(pontos)
    forma = py5.create_shape()
    with forma.begin_closed_shape():
        for x, y in vertices[0]:
            forma.vertex(x, y)
        with forma.begin_contour():
            for x, y in vertices[1][::-1]:
                forma.vertex(x, y)
    return forma


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(FUNDO)
    py5.shape_mode(py5.CORNER)
    meio = T * T * T + (T * (T + T + T + T))
    passo = T * T
    ri = int(T // T)
    rf = int((T * T * T) + (T * T * T) + (passo * T))
    with py5.push_matrix():
        py5.translate(meio, meio - T, -T)
        for idx, raio in enumerate(range(ri, rf, int(passo))):
            larg = passo
            forma = cria_forma(raio, larg)
            cor = PALETA[0]
            forma.set_stroke_weight(py5.random_gaussian(6))
            forma.set_stroke(cor)
            forma.set_fill(cor)
            py5.shape(forma, ri, ri)
            rotacao = ri if int(idx % T) == ri else int(py5.random_gaussian(int(T)))
            PALETA.rotate(rotacao)

    helpers.write_legend(sketch=sketch, frame="#000", cor="#FFF")


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    helpers.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
