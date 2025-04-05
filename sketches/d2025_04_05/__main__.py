"""2025-04-05
Padrões 04
Padrão de traços em grade com paleta inspirada em Warhol
png
Sketch,py5,CreativeCoding
"""

import py5

from utils import helpers
from utils.draw import cria_grade, gera_paleta

sketch = helpers.info_for_sketch(__file__, __doc__)

TAMANHO_X = 96
TAMANHO_Y = 96


def padrao_01(pg: py5.Py5Graphics, meio_x: float, meio_y: float) -> None:
    pg.stroke_weight(2)
    pg.no_fill()
    pg.ellipse_mode(py5.CENTER)
    for d in range(5, TAMANHO_X * 2 - 5, 20):
        pg.circle(meio_x, meio_y, d)


def padrao_02(pg: py5.Py5Graphics, meio_x: float, meio_y: float) -> None:
    pg.stroke_weight(2)
    for x in range(-meio_x + 3, meio_x, 10):
        pg.line(x, -meio_y, x, meio_y)


def desenha_padrao(
    padrao_id: int, angulo: int, cor_fundo: py5.Py5Color, cor_traco: py5.Py5Color
) -> py5.Py5Graphics:
    pg = py5.create_graphics(TAMANHO_X, TAMANHO_Y, py5.P3D)
    func = globals()[f"padrao_{padrao_id:02d}"]
    with pg.begin_draw():
        meio_x = TAMANHO_X // 2
        meio_y = TAMANHO_Y // 2
        with pg.push_matrix():
            pg.translate(meio_x, meio_y)
            pg.rotate(angulo)
            pg.background(cor_fundo)
            pg.stroke(cor_traco)
            func(pg, meio_x, meio_y)
            pg.rotate(-angulo)
    return pg


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.rect_mode(py5.CENTER)
    idx = 0
    celula = 100
    grade = cria_grade(py5.width, py5.height, 50, 50, celula, celula, False)
    paleta = gera_paleta("Warhol", True)
    angulos = (0, 90, 180, 270)
    padroes = (1, 2)
    rotacao_paleta = (1, 2, 3)
    for x, y in grade:
        padrao_id = py5.random_choice(padroes)
        graus = py5.radians(py5.random_choice(angulos))
        cor_fundo = paleta[0]
        cor_traco = py5.color("#FFF")
        padrao = desenha_padrao(padrao_id, graus, cor_fundo, cor_traco)
        py5.image(padrao, x, y)
        idx += 1
        paleta.rotate(py5.random_choice(rotacao_paleta))
    with py5.push():
        py5.translate(py5.width / 2, py5.height / 2, -120)
        py5.fill("#000")
        py5.rect(0, 0, py5.width * 1.2, py5.height * 1.2)
    helpers.write_legend(sketch=sketch, frame="#000")


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
