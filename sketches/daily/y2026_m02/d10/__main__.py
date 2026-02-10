"""2026-02-10
Pattern & Grid 04
Grade de padrões geométricos
ericof.com|https://openprocessing.org/sketch/1726494
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.grade import cria_grade
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

PALETAS = [
    gera_paleta("south-africa"),
]

CELULAS = 6
MULT_CELULA = 0.90
MULT_FORMA = 0.75
REPET_FORMA = 14


def forma(x: float, y: float, d: float, palette: list[int]):
    r = d / 2
    hr = r / 2
    aa = py5.TAU / REPET_FORMA

    size = max(2, int(r))
    pg = py5.create_graphics(size, size)

    # Desenho da forma base
    with pg.begin_draw():
        pg.rect_mode(py5.CENTER)
        pg.background(py5.color(palette[0]))
        pg.no_stroke()

        c = int(py5.random(3, 6))
        w = pg.width / c
        t = int(py5.random(3))

        for i in range(c):
            for j in range(c):
                col = palette[1 + int(py5.random(len(palette) - 1))]
                pg.fill(py5.color(col))
                func = pg.square if t == 0 else pg.circle
                func(i * w + w / 2, j * w + w / 2, w * py5.random(0.5, 1))

    # Máscara
    mg = py5.create_graphics(size, size)
    with mg.begin_draw():
        mg.background(255)
        mg.no_stroke()
        mg.fill(0)

        with mg.begin_shape():
            step = py5.TAU / 180
            a = -aa
            while a < py5.PI:
                mg.vertex(
                    mg.width / 2 + hr * py5.cos(a),
                    mg.height / 2 + hr * py5.sin(a),
                )
                a += step

            a = aa * 2
            while a > 0:
                mg.vertex(
                    hr * py5.cos(-aa) + hr * py5.cos(a),
                    mg.height / 2 + hr * py5.sin(-aa) + hr * py5.sin(a),
                )
                a -= step

    # --- apply mask directly to PGraphics ---
    pg.mask(mg)

    # --- draw n rotated copies ---
    with py5.push_matrix():
        py5.translate(x, y)
        for _ in range(REPET_FORMA):
            py5.image(pg, r * 0.5, 0, pg.width + 1, pg.height + 1)
            py5.rotate(py5.TAU / REPET_FORMA)


def celula(
    x: float,
    y: float,
    celula_x: float,
    paleta: list[int],
    cor_fundo_celula: int,
):
    with py5.push():
        cor = py5.random_choice(paleta)
        py5.fill(cor)
        tamanho = celula_x * MULT_CELULA
        py5.circle(x, y, tamanho)
        with py5.push():
            py5.fill(cor_fundo_celula)
            py5.stroke(cor_fundo_celula)
            py5.circle(x, y, tamanho * 0.95)
        tamanho = celula_x * MULT_FORMA
        py5.fill(cor)
        forma(x, y, tamanho, paleta)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.rect_mode(py5.CENTER)
    py5.image_mode(py5.CENTER)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(cor_fundo)
    largura, altura = helpers.DIMENSOES.internal
    celula_x = largura // CELULAS
    celula_y = altura // CELULAS
    meia_celula_x = celula_x / 2
    meia_celula_y = celula_y / 2
    grade = cria_grade(
        largura=largura,
        altura=altura,
        margem_x=0,
        margem_y=0,
        celula_x=celula_x,
        celula_y=celula_y,
        alternada=False,
    )
    cor_fundo_celula = py5.color("#000")
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, -10)
        for xb, yb in grade:
            x, y = xb + meia_celula_x, yb + meia_celula_y
            paleta = py5.random_choice(PALETAS)
            celula(x, y, celula_x, paleta, cor_fundo_celula)
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
