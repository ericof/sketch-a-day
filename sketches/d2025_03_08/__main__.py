"""2025-03-08
Rotatio XXI
Rotações de retângulos com grade e diversos níveis
png
Sketch,py5,CreativeCoding
"""

from collections import deque

import py5

from utils import helpers
from utils.draw import cria_grade_ex, gera_paleta

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
    pg.ellipse_mode(py5.CENTER)
    direcao = 1
    tamanho_paleta = len(paleta)
    angulo_final = voltas * 360
    with pg.begin_draw():
        pg.no_stroke()
        for profundidade in range(-50, -10, 10):
            with pg.push_matrix():
                pg.translate(xc, yc, profundidade)
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
    py5.rect_mode(py5.CORNER)
    py5.blend_mode(py5.BLEND)
    alt = 80
    larg = 80
    grade = cria_grade_ex(py5.width, py5.height, 0, 0, alt, larg, False)
    paletas = deque(
        [
            gera_paleta("laranja", True),
            gera_paleta("sunset-ocean", True),
        ]
    )
    paletas.rotate(py5.random_int(len(paletas)))
    paleta = paletas[0]
    rot = py5.random_gaussian(30, 5)
    rot_passo = py5.random_gaussian(-5, 2)
    razao_larg_alt = py5.random(0.4, 0.9)
    voltas = py5.random_int(3, 8)
    passo = py5.random(0.75, 0.90)
    diametro = 1200
    idt = 0
    paleta = paletas[0]
    for idx, x, idy, y in grade:
        if idx == 0:
            paletas.rotate()
        paleta = paletas[idx % 2]
        xf = x + larg
        yf = y + alt
        params = [
            paleta,
            rot,
            rot_passo,
            diametro,
            py5.width,
            py5.height,
            200,
            400,
            razao_larg_alt,
            voltas,
            passo,
        ]
        with py5.push_matrix():
            py5.translate(0, 0, -10)
            with py5.push_style():
                img_array = rotatio(*params).get_np_pixels()[y:yf, x:xf]
                image = py5.create_image_from_numpy(img_array)
                py5.image(image, x, y, larg, alt)
            with py5.push_style():
                py5.stroke("#777")
                py5.stroke_weight(3)
                py5.no_fill()
                py5.rect(x, y, larg, alt)
        idt += 1
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
