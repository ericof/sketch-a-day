"""2026-06-18
Caquinhos / Ladrilhos 16
Homenagem aos pisos de caquinhos de São Paulo.
ericof.com|https://ericof.com/en/sketches/2023-05-09
png
Sketch,py5,CreativeCoding
"""

from opensimplex import OpenSimplex
from sketches.utils.draw import canvas
from sketches.utils.draw.grade import cria_grade_ex
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0, 0, 0)
cor_fundo_interna = py5.color(60, 60, 45)

celula_x = 10
celula_y = 10
lado_min_mult = 2.1
lado_max_mult = 4.5
mult_x = 25
mult_y = 25
borda = 0.20
faixa_bagunca = 40

lado_min = int(max(celula_x, celula_y) * lado_min_mult)
lado_max = int(max(celula_x, celula_y) * lado_max_mult)
tamanho = lado_max

noise_generator = OpenSimplex(seed=py5.random_int(20_000))

formas: list[tuple[float, float, int, int, int, py5.Py5Shape]] = []


def par_bagunca(faixa_bagunca: int) -> tuple[float, float]:
    bx = py5.random(-faixa_bagunca, faixa_bagunca)
    by = py5.random(-faixa_bagunca, faixa_bagunca)
    return bx, by


def caco(
    x: float,
    y: float,
    tamanho: int,
    faixa_bagunca: int,
    cor_interna: int,
    cor_externa: int,
) -> py5.Py5Shape:
    s = py5.create_shape(py5.GROUP)
    bx, by = par_bagunca(faixa_bagunca)
    x0, y0 = x - tamanho / 2 + bx, y - tamanho / 2 + by
    bx, by = par_bagunca(faixa_bagunca)
    x1, y1 = x + tamanho / 2 + bx, y - tamanho / 2 + by
    bx, by = par_bagunca(faixa_bagunca)
    x2, y2 = x + tamanho / 2 + bx, y + tamanho / 2 + by
    bx, by = par_bagunca(faixa_bagunca)
    x3, y3 = x - tamanho / 2 + bx, y + tamanho / 2 + by
    for cor, escala in ((cor_externa, 1 + borda), (cor_interna, 1)):
        forma = py5.create_shape()
        forma.set_fill(cor)
        forma.set_stroke_weight(0)
        with forma.begin_closed_shape():
            forma.vertex(x + (x0 - x) * escala, y + (y0 - y) * escala)
            forma.vertex(x + (x1 - x) * escala, y + (y1 - y) * escala)
            forma.vertex(x + (x2 - x) * escala, y + (y2 - y) * escala)
            forma.vertex(x + (x3 - x) * escala, y + (y3 - y) * escala)
        s.add_child(forma)
    return s


def cor_caco(idx: int, idy: int) -> int:
    total = idx + idy
    cor = py5.color(152, 59, 47)
    if total % 10 == 0:
        cor = py5.color(0)
    elif total % 7 == 0:
        cor = py5.color(218, 160, 57)
    return cor


def popula_forma(
    largura: int,
    altura: int,
    celula_x: int,
    celula_y: int,
    mult_x: float = 15,
    mult_y: float = 10,
) -> list[tuple[float, float, int, int, int, py5.Py5Shape]]:
    formas = []
    for idx, x0, idy, y0 in cria_grade_ex(
        largura, altura, 0, 0, celula_x, celula_y, True
    ):
        z = py5.random_int(0, 5)
        noise = noise_generator.noise2(x0, y0)
        if idx == 0 or idy == 0:
            y = y0
            x = x0
        else:
            y = y0 + (mult_y * noise)
            x = x0 + (mult_x * noise)
        largura = py5.random_int(lado_min, lado_max)
        altura = py5.random_int(lado_min, lado_max)
        forma = caco(
            0,
            0,
            tamanho,
            faixa_bagunca,
            cor_interna=cor_caco(idx, idy),
            cor_externa=cor_fundo_interna,
        )
        formas.append((x, y, z, largura, altura, forma))
    return formas


def inicializa():
    global formas, lado_min, lado_max, tamanho
    lado_min = int(max(celula_x, celula_y) * lado_min_mult)
    lado_max = int(max(celula_x, celula_y) * lado_max_mult)
    tamanho = lado_max
    formas = popula_forma(
        *helpers.DIMENSOES.internal, celula_x, celula_y, mult_x, mult_y
    )


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
        py5.translate(*helpers.DIMENSOES.pos_interno, -5)
        desenha_fundo(cor_fundo_interna)
        for x, y, z, largura, altura, forma in formas:
            with py5.push():
                py5.translate(x, y, z)
                py5.shape(forma, celula_x / 2, celula_y / 2, largura, altura)
    msg = (
        f"celula (x - y): {celula_x} - {celula_y} | "
        f"lado (min - max): {lado_min_mult} - {lado_max_mult} | "
        f"borda: {borda:.2f}"
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
    global lado_min_mult, lado_max_mult, celula_x, celula_y, borda
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
        case "w":
            borda += 0.1
            inicializa()
        case "s":
            diff = 0.1 if borda > 0.2 else 0.0
            borda -= diff
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
