"""2024-01-20
Genuary 20 - Generative typography.
Texto #Genuary2024 escrito com formas distorcidas a partir da fonte Konami.
png
Sketch,py5,CreativeCoding,genuary,genuary20
"""
import string

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

CARACTERES = string.ascii_letters + "#" + string.digits
FONTE = None
FORMAS = None
TEXTO = []


def bagunca_fonte(base: py5.Py5Shape):
    for idx in range(base.get_vertex_count()):
        v = base.get_vertex(idx)
        v.x += py5.random_gaussian(-5, 5)
        v.y += py5.random_gaussian(-1, 1)
        base.set_vertex(idx, v)
    return base


def setup():
    global FONTE
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.shape_mode(py5.CENTER)
    # Require the KonamiWaiWaiWorldFamicomExtended font to be installed
    FONTE = py5.create_font("KonamiWaiWaiWorldFamicomExtended", 45)
    texto = "#Genuary2024"
    for c in texto:
        forma = FONTE.get_shape(c)
        forma.disable_style()
        forma = bagunca_fonte(forma)
        largura = forma.get_width()
        TEXTO.append((forma, largura))


def draw():
    espacamento = 5
    total = len(TEXTO)
    largura = sum([i[1] for i in TEXTO]) + espacamento * total
    x = -(largura / 2)
    py5.fill("#FFF")
    py5.stroke("#FFF")
    with py5.push_matrix():
        py5.translate(py5.width / 2, py5.height / 2)
        for forma, l in TEXTO:
            py5.shape(forma, x, 0)
            x += l + espacamento
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
