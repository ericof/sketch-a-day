"""2025-02-09
MSX Lives 03
Logo do MSX e cores básicas de um MSX 1
png
Sketch,py5,CreativeCoding
"""

from pathlib import Path

import py5

from utils import helpers
from utils.draw import cria_grade_ex, gera_octagono

sketch = helpers.info_for_sketch(__file__, __doc__)

LOGO_FILE = Path(__file__).parent / "msx-logo.svg"

PALETA = [
    "#000000",
    "#010101",
    "#3eb849",
    "#74d07d",
    "#5955e0",
    "#8076f1",
    "#b95e51",
    "#65dbef",
    "#db6559",
    "#ff897d",
    "#ccc35e",
    "#ded087",
    "#3aa241",
    "#b766b5",
    "#cccccc",
    "#ffffff",
]


def desenha_fundo():
    passo = py5.height // len(PALETA)
    x0, xf = -py5.width * 2, py5.width * 2
    with py5.push_matrix(), py5.push_style():
        py5.translate(0, 0, -80)
        py5.no_stroke()
        for idy, y in enumerate(range(0, py5.height, passo)):
            y0 = y - passo
            yf = y + 2 * passo
            py5.fill(PALETA[idy])
            py5.rect(x0, y0, xf, yf)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    desenha_fundo()
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CENTER)
    forma = py5.load_shape(LOGO_FILE)
    aspect_ratio = forma.width / forma.height
    celula_largura = 150
    celula_altura = celula_largura
    forma_largura = celula_largura * 0.8
    forma_altura = forma_largura / aspect_ratio
    grade = cria_grade_ex(py5.width, py5.height, 100, 100, 150, 150, False)
    h = 245
    py5.shape_mode(py5.CENTER)
    for idx, x, idy, y in grade:
        fundo = gera_octagono()
        s = py5.remap(idy, 0, 3, 50, 91)
        b = py5.remap(idx, 0, 3, 50, 97)
        with py5.push_matrix():
            py5.translate(x, y, -60)
            with py5.push_style():
                fundo.set_stroke(py5.color(h, s, b * 0.9))
                fundo.set_stroke_weight(5)
                fundo.set_fill(py5.color(h, s, b))
                py5.shape(
                    fundo,
                    celula_largura * 1.2,
                    celula_altura / 2,
                    celula_largura,
                    celula_altura,
                )
    py5.shape_mode(py5.CENTER)
    py5.no_stroke()
    for idx, xb, idy, yb in grade:
        x = xb + celula_largura / 2
        y = yb + celula_altura / 2
        with py5.push_matrix():
            py5.translate(x, y, -60)
            with py5.push_style():
                py5.fill(py5.color(100, 0, 0))
                py5.rect(0, 0, forma_largura, forma_altura)
            py5.shape(forma, 0, 0, forma_largura, forma_altura)
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
