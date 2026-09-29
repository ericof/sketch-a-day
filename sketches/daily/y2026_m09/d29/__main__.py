"""2026-09-29
Padrões 25
Exercício de padrões coloridos
ericof.com
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from sketches.utils.draw import canvas
from sketches.utils.draw.grade import cria_grade
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

largura_x = 160
altura_y = 160
margem_x = 0
margem_y = 0
padrao_largura = largura_x * 0.6
padrao_altura = altura_y * 0.6
densidade = 2
angulos = [0, 90, 180, 270]


def cria_forma(x: float, y: float, largura: float, largura_i: float) -> py5.PShape:
    x1 = x + largura
    y1 = y + largura
    # Interno
    buffer_i = (largura - largura_i) / 2
    xi0 = x + buffer_i
    xi1 = xi0 + largura_i
    xih = (xi1 - xi0) / 2
    yi0 = y + buffer_i
    yi1 = yi0 + largura_i
    yih = (yi1 - yi0) / 2
    xbz1 = xi0 + ((largura_i / 2) * 0.45)
    xbz2 = xi1 - ((largura_i / 2) * 0.45)
    ybz1 = yi0 + ((largura_i / 2) * 0.45)
    ybz2 = yi1 - ((largura_i / 2) * 0.45)
    s = py5.create_shape()
    s.set_fill(False)
    s.set_stroke_weight(3)
    with s.begin_shape():
        s.vertex(x, y)
        s.vertex(x1, y)
        s.vertex(x1, y1)
        s.vertex(x, y1)
        s.vertex(x, y)
        with s.begin_contour():
            s.vertex(xi0, yih)
            s.bezier_vertex(xi0, ybz1, xbz1, yi0, xih, yi0)
            s.bezier_vertex(xbz2, yi0, xi1, ybz1, xi1, yih)
            s.bezier_vertex(xi1, ybz2, xbz2, yi1, xih, yi1)
            s.bezier_vertex(xbz1, yi1, xi0, ybz2, xi0, yih)

    return s


def cria_celula(
    largura: float, altura: float, forma: py5.PShape, rotacao: float, cores: tuple
) -> py5.Py5Image:
    pg = py5.create_graphics(int(largura), int(altura), py5.P3D)
    pg.shape_mode(py5.CENTER)
    centro = (largura / 2, altura / 2)
    with pg.begin_draw():
        pg.background(cores[1])
        forma.set_fill(cores[2])
        forma.set_stroke(cores[0])
        with pg.push():
            pg.translate(*centro)
            pg.rotate_z(py5.radians(rotacao))
            pg.shape(forma)
    pg.load_pixels()
    imagem = py5.create_image(pg.pixel_width, pg.pixel_height, py5.ARGB)
    imagem.load_pixels()
    imagem.pixels[:] = pg.pixels[:]
    imagem.update_pixels()
    return imagem


def inicializa():
    forma = cria_forma(0, 0, largura_x, padrao_largura)
    posicoes = cria_grade(
        *helpers.DIMENSOES.internal, margem_x, margem_y, largura_x, altura_y, False
    )
    paleta = deque([
        "#f71735",
        "#067bc2",
        "#FFC247",
        "#f654a9",
        "#2F0A30",
    ])
    grade = []
    for x, y in posicoes:
        z = py5.random_int(-1, 1)
        rotacao = py5.random_choice(angulos)
        cores = (
            py5.color(paleta[0]),
            py5.color(paleta[1]),
            py5.color(paleta[2]),
        )
        imagem = cria_celula(largura_x, altura_y, forma, rotacao, cores)
        paleta.rotate(py5.random_int(-2, 2))
        grade.append((x, y, z, imagem))
    return grade


def setup():
    global grade
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    grade = inicializa()


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(0, 0, -2)
        for x, y, z, imagem in grade:
            # A imagem foi rasterizada em `densidade`x e tem o lado desse
            # tamanho; o destino explicito a traz de volta ao tamanho nominal.
            with py5.push():
                py5.translate(*helpers.DIMENSOES.pos_interno, z)
                py5.image(
                    imagem,
                    x,
                    y,
                    largura_x,
                    altura_y,
                )
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
