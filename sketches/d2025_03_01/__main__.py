"""2025-03-01
Rotatio XIV
Rotações de retângulos com paleta em tons de laranja
png
Sketch,py5,CreativeCoding
"""

from collections import deque

import py5

from utils import helpers
from utils.draw import cria_grade_ex, gera_paleta, lista_paletas

sketch = helpers.info_for_sketch(__file__, __doc__)


def rotatio(
    paleta: list | deque,
    rot: int,
    rot_passo: int,
    diametro: float,
    larg: float,
    alt: float,
    xc: float,
    yc: float,
    razao_larg_alt: float,
    voltas: float,
    passo: float,
) -> py5.Py5Graphics:
    pg = py5.create_graphics(larg, alt, py5.P3D)
    pg.rect_mode(py5.CENTER)
    direcao = 1
    tamanho_paleta = len(paleta)
    angulo_final = voltas * 360
    with pg.begin_draw():
        pg.no_stroke()
        with pg.push_matrix():
            pg.translate(xc, yc, -30)
            idx = 0
            while diametro > 5:
                if idx and idx % tamanho_paleta == 0:
                    direcao *= -1
                    rot += rot_passo
                angulo = 0
                cor = paleta[tamanho_paleta // 2]
                paleta.rotate(direcao)
                pg.fill(cor)
                while angulo < angulo_final:
                    pg.rotate_z(py5.radians(rot))
                    altura = diametro * razao_larg_alt
                    pg.rect(0, 0, diametro, altura)
                    angulo += abs(rot)
                idx += 1
                diametro *= passo
    return pg


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CENTER)
    py5.blend_mode(py5.BLEND)
    alt = 100
    larg = 100
    grade = cria_grade_ex(py5.width, py5.height, 50, 50, alt, larg, False)
    paletas = deque([gera_paleta(paleta, True) for paleta in lista_paletas()])
    paletas.rotate(py5.random_int(len(paletas)))
    paleta = paletas[0]
    rot = py5.random_gaussian(-30, 10)
    rot_passo = py5.random_gaussian(10, 5)
    razao_larg_alt = py5.random(0.5, 0.9)
    voltas = py5.random_int(3, 5)
    passo = py5.random(0.75, 0.90)
    diametro = 400
    idt = 0
    for idx, x, idy, y in grade:
        paletas.rotate()
        paleta = paletas[0]
        xc = (py5.width // 2) - x
        yc = (py5.height // 2) - y
        params = [
            paleta,
            rot,
            rot_passo,
            diametro,
            larg,
            alt,
            xc,
            yc,
            razao_larg_alt,
            voltas,
            passo,
        ]
        with py5.push_style():
            image = rotatio(*params)
            py5.image(image, x, y, larg, alt)
        idt += 1
        with py5.push_style():
            py5.no_fill()
            py5.stroke_weight(2)
            py5.stroke("#111")
            if idx == idy == 3:
                py5.stroke_weight(4)
                py5.stroke("#ff0080")

            py5.rect(x + larg / 2, y + alt / 2, larg, alt)
    helpers.write_legend(sketch=sketch)


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
