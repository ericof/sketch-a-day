"""2026-06-02
Caquinhos / Ladrilhos 01
Homenagem aos pisos de caquinhos de São Paulo.
ericof.com|https://ericof.com/en/sketches/2023-05-09
png
Sketch,py5,CreativeCoding
"""

from opensimplex import OpenSimplex
from random import shuffle
from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
cor_fundo_interna = py5.color(226, 214, 187)

# Configura o OpenSimplex para gerar os valores de ruido usados na
# rotacao dos caquinhos.
noise_generator = OpenSimplex(seed=3245)

formas: list[tuple[float, float, int, int, py5.Py5Shape]] = []


def par_bagunca(faixa_bagunca: int) -> tuple[float, float]:
    bx = py5.random(-faixa_bagunca, faixa_bagunca)
    by = py5.random(-faixa_bagunca, faixa_bagunca)
    return bx, by


def caco(x: float, y: float, lado: int, faixa_bagunca: int) -> py5.Py5Shape:
    bx, by = par_bagunca(faixa_bagunca)
    x0, y0 = x - lado / 2 + bx, y - lado / 2 + by
    bx, by = par_bagunca(faixa_bagunca)
    x1, y1 = x + lado / 2 + bx, y - lado / 2 + by
    bx, by = par_bagunca(faixa_bagunca)
    x2, y2 = x + lado / 2 + bx, y + lado / 2 + by
    bx, by = par_bagunca(faixa_bagunca)
    x3, y3 = x - lado / 2 + bx, y + lado / 2 + by
    s = py5.create_shape()
    with s.begin_closed_shape():
        s.vertex(x0, y0)
        s.vertex(x1, y1)
        s.vertex(x2, y2)
        s.vertex(x3, y3)
    return s


def calcula_pontos(
    altura: int, largura: int, passo: int
) -> list[tuple[float, float, int]]:
    pontos = []
    for y0 in range(10, altura, passo):
        for x0 in range(10, largura, passo):
            noise = noise_generator.noise2(x0, y0)
            y = y0 + (10 * noise)
            x = x0 + (15 * noise)
            stroke = py5.random_int(1, 4)
            pontos.append((x, y, stroke))
    shuffle(pontos)
    return pontos


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    pontos = calcula_pontos(*helpers.DIMENSOES.internal, 30)
    for idx, (x, y, stroke) in enumerate(pontos):
        lado = py5.random_int(30, 35)
        cor = py5.color(152, 59, 47)
        if idx % 3 == 0:
            cor = py5.color(0)
        elif idx % 4 == 0:
            cor = py5.color(218, 160, 57)
        forma = caco(0, 0, 20, 7)
        forma.set_fill(cor)
        forma.set_stroke(cor)
        formas.append((x, y, stroke, lado, forma))


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, -10)
        with py5.push():
            py5.fill(cor_fundo_interna)
            py5.no_stroke()
            py5.rect(0, 0, *helpers.DIMENSOES.internal)
        for x, y, stroke, lado, forma in formas:
            py5.stroke(cor_fundo_interna)
            py5.stroke_weight(stroke)
            with py5.push():
                py5.translate(x, y, 3)
                py5.shape(forma, 0, 0, lado, lado)
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
