"""2026-06-05
Caquinhos / Ladrilhos 04
Homenagem aos pisos de caquinhos de São Paulo.
ericof.com|https://ericof.com/en/sketches/2023-05-09
png
Sketch,py5,CreativeCoding
"""

from opensimplex import OpenSimplex
from random import shuffle
from sketches.utils.draw import canvas
from sketches.utils.draw.grade import cria_grade
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
cor_fundo_interna = py5.color(226, 214, 187)

celula_x = 40
celula_y = 40
lado_min_mult = 1.5
lado_max_mult = 2.5
traco_min_div = 15
traco_max_div = 6
mult_x = 15
mult_y = 15

lado_min = int(max(celula_x, celula_y) * lado_min_mult)
lado_max = int(max(celula_x, celula_y) * lado_max_mult)
traco_min = max(celula_x, celula_y) // traco_min_div
traco_max = max(celula_x, celula_y) // traco_max_div
tamanho = lado_max


noise_generator = OpenSimplex(seed=py5.random_int(10_000))

formas: list[tuple[float, float, int, int, int, py5.Py5Shape]] = []


def par_bagunca(faixa_bagunca: int) -> tuple[float, float]:
    bx = py5.random(-faixa_bagunca, faixa_bagunca)
    by = py5.random(-faixa_bagunca, faixa_bagunca)
    return bx, by


def caco(x: float, y: float, tamanho: int, faixa_bagunca: int) -> py5.Py5Shape:
    bx, by = par_bagunca(faixa_bagunca)
    x0, y0 = x - tamanho / 2 + bx, y - tamanho / 2 + by
    bx, by = par_bagunca(faixa_bagunca)
    x1, y1 = x + tamanho / 2 + bx, y - tamanho / 2 + by
    bx, by = par_bagunca(faixa_bagunca)
    x2, y2 = x + tamanho / 2 + bx, y + tamanho / 2 + by
    bx, by = par_bagunca(faixa_bagunca)
    x3, y3 = x - tamanho / 2 + bx, y + tamanho / 2 + by
    s = py5.create_shape()
    with s.begin_closed_shape():
        s.vertex(x0, y0)
        s.vertex(x1, y1)
        s.vertex(x2, y2)
        s.vertex(x3, y3)
    return s


def calcula_pontos(
    largura: int,
    altura: int,
    celula_x: int,
    celula_y: int,
    mult_x: float = 15,
    mult_y: float = 10,
) -> list[tuple[float, float, int, int]]:
    pontos = []
    for x0, y0 in cria_grade(largura, altura, 0, 0, celula_x, celula_y, True):
        z = py5.random_int(0, 5)
        noise = noise_generator.noise2(x0, y0)
        y = y0 + (mult_y * noise)
        x = x0 + (mult_x * noise)
        traco = py5.random_int(traco_min, traco_max)
        pontos.append((x, y, z, traco))
    shuffle(pontos)
    return pontos


def cor_caco(idx: int) -> int:
    cor = py5.color(152, 59, 47)
    if idx % 3 == 0:
        cor = py5.color(0)
    elif idx % 4 == 0:
        cor = py5.color(218, 160, 57)
    return cor


def inicializa():
    global formas
    formas = []
    pontos = calcula_pontos(
        *helpers.DIMENSOES.internal, celula_x, celula_y, mult_x, mult_y
    )
    for idx, (x, y, z, traco) in enumerate(pontos):
        largura = py5.random_int(lado_min, lado_max)
        altura = py5.random_int(lado_min, lado_max)
        cor = cor_caco(idx)
        forma = caco(0, 0, tamanho, 40)
        forma.set_fill(cor)
        forma.set_stroke_weight(traco)
        forma.set_stroke(cor_fundo_interna)
        formas.append((x, y, z, largura, altura, forma))


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    inicializa()


def desenha_fundo(cor: int):
    """Desenha o fundo por baixo dos caquinhos."""
    with py5.push():
        py5.fill(cor)
        py5.no_stroke()
        py5.rect(0, 0, *helpers.DIMENSOES.internal)


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, -10)
        desenha_fundo(cor_fundo_interna)
        for x, y, z, largura, altura, forma in formas:
            with py5.push():
                py5.translate(x, y, z)
                py5.shape(forma, celula_x / 2, celula_y / 2, largura, altura)
    msg = (
        f"celula (x - y): {celula_x} - {celula_y} | "
        f"lado (min - max): {lado_min} - {lado_max} | "
        f"traco (min - max): {traco_min} - {traco_max}"
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
    global lado_min_mult, lado_max_mult, celula_x, celula_y
    key = py5.key
    match key:
        case "r":
            inicializa()
        case ">":
            celula_x += 2
            celula_y += 2
            inicializa()
        case "<":
            celula_x -= 2
            celula_y -= 2
            inicializa()
        case "+":
            lado_min_mult *= 1.1
            lado_max_mult *= 1.1
            inicializa()
        case "-":
            lado_min_mult *= 0.9
            lado_max_mult *= 0.9
            inicializa()
        case " ":
            save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
