"""2025-01-05
Isometric art - Proto City
Desenho com caixas de diversos tamanhos dispostas representando uma cidade
png
Sketch,py5,CreativeCoding,genuary,genuary5
"""

from contextlib import contextmanager

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

ISO_X = helpers.LARGURA // 2
ISO_Y = helpers.ALTURA // 2
ISO_Z = -800

ROTACAO_X = py5.radians(-30)
ROTACAO_Y = py5.radians(-60)

LIMITES_CHAO = (0, 0, 8000, 8000), (0, 0, 8000, 8000)
LIMITES_CIDADE = -4000, 4000

DIMENSOES = (
    (10, 30, False),
    (10, 30, False),
    (10, 30, False),
    (10, 30, False),
    (10, 30, False),
    (10, 30, False),
    (30, 10, False),
    (30, 10, False),
    (30, 10, False),
    (30, 10, False),
    (30, 10, False),
    (40, 20, False),
    (40, 20, False),
    (40, 20, False),
    (40, 20, False),
    (40, 20, False),
    (40, 20, False),
    (40, 20, False),
    (40, 20, False),
    (30, 30, True),
    (40, 40, True),
    (40, 90, False),
    (70, 110, False),
    (75, 115, False),
    (30, 90, False),
    (80, 120, False),
    (50, 140, False),
    (60, 100, False),
)
PALETAS = (
    (
        "#ECEBDE",
        "#D7D3BF",
        "#D7D3BF",
    ),
    (
        "#D7D3BF",
        "#C1BAA1",
        "#C1BAA1",
    ),
    (
        "#C1BAA1",
        "#A59D84",
        "#A59D84",
    ),
    (
        "#A59D84",
        "#A59D90",
        "#A59D84",
    ),
    (
        "#E7D4B5",
        "#A0937D",
        "#B6C7AA",
    ),
    (
        "#A0937D",
        "#E7D4B5",
        "#B6C7AA",
    ),
    (
        "#3C3D37",
        "#1E201E",
        "#1E201E",
    ),
)


@contextmanager
def isometric(altura=0, *args, **kwargs):
    py5.push_matrix()
    py5.translate(ISO_X, ISO_Y, ISO_Z)
    py5.rotate_x(ROTACAO_X)
    py5.rotate_y(ROTACAO_Y)
    py5.translate(0, -altura, 0)
    yield None
    py5.pop_matrix()


def desenha_chao():
    with py5.push_style():
        with isometric():
            py5.rotate_x(py5.radians(-90))
            py5.rect_mode(py5.CENTER)
            py5.fill(0, 0, 80)
            py5.rect(*LIMITES_CHAO[1])
            py5.translate(0, 0, 5)
            py5.fill(120, 100, 67)
            py5.rect(*LIMITES_CHAO[0])


def desenha_predio(
    x, y, z, com_cupula=False, largura=300, profundidade=300, altura=300
):
    paleta = py5.random_choice(PALETAS)
    # Base
    with py5.push_style():
        with isometric(altura / 2):
            py5.translate(x, y, z)
            py5.fill(paleta[0])
            py5.stroke(paleta[1])
            py5.box(largura, altura, profundidade)

    raio = (altura // 2) * 0.9
    yc = raio * 0.8
    if com_cupula:
        # Cupula
        with py5.push_style():
            py5.no_stroke()
            with isometric(altura / 2):
                py5.translate(x, yc, z)
                py5.fill(paleta[2])
                py5.sphere(raio)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.sphere_detail(100)
    py5.no_stroke()
    desenha_chao()
    py5.stroke_weight(2)
    x = LIMITES_CIDADE[0]
    while x < LIMITES_CIDADE[1]:
        profundidade_max = py5.random_int(40, 120)
        buffer_x = py5.random_int(10, 40)
        z = LIMITES_CIDADE[0]
        while z < LIMITES_CIDADE[1]:
            largura, altura, com_cupula = py5.random_choice(DIMENSOES)
            buffer_z = py5.random_int(5, largura // 2)
            z += buffer_z + largura // 2
            if z < LIMITES_CIDADE[1]:
                profundidade = (
                    py5.random_int(largura, profundidade_max)
                    if largura <= profundidade_max
                    else largura
                )
                if x < -3000:
                    altura *= py5.random(1, 2.3)
                if z > 3000:
                    altura *= py5.random(1, 3.3)
                desenha_predio(x, 0, z, com_cupula, largura, profundidade, altura)
            z += largura
        x += profundidade_max + buffer_x

    helpers.write_legend(sketch=sketch, frame="#000", cor="#fff")


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
