"""2026-07-20
Formas Geométricas 01
Exercício de grade de formas geométricas
ericof.com|https://ericof.com/en/sketches/2024-06-29
png
Sketch,py5,CreativeCoding
"""

from random import shuffle
from sketches.padroes.poligonos import gera_poligono_regular
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.grade import cria_grade_ex
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

celula_x: int = 45
celula_y: int = 20
forma_escala: float = 1.11
alternada: bool = True
preencher: bool = True

traco: float = 4.2
cor_traco_preenchido = py5.color(0, 0, 0, 0.2)
traco_preenchido: float = 1.5


def inicializa():
    global formas, grade
    grade = cria_grade_ex(
        *helpers.DIMENSOES.external, 0, 0, celula_x, celula_y, alternada=alternada
    )
    formas = [
        gera_poligono_regular(8, celula_x * forma_escala, celula_y * forma_escala),
        gera_poligono_regular(6, celula_x * forma_escala, celula_y * forma_escala),
        gera_poligono_regular(8, celula_x * forma_escala, celula_y * forma_escala),
        gera_poligono_regular(6, celula_x * forma_escala, celula_y * forma_escala),
        gera_poligono_regular(6, celula_x * forma_escala, celula_y * forma_escala),
        gera_poligono_regular(8, celula_x * forma_escala, celula_y * forma_escala),
    ]
    shuffle(formas)
    shuffle(grade)


def setup():
    global formas, grade
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.shape_mode(py5.CENTER)
    inicializa()


def draw():
    py5.background(cor_fundo)
    paleta = gera_paleta("op-2363803", True)
    total_formas = len(formas)
    with py5.push():
        py5.translate(0, 0, -10)
        for idx, x, idy, y in grade:
            index = (idx + idy) % total_formas
            forma = formas[index]
            if preencher:
                forma.set_fill(paleta[0])
                forma.set_stroke_weight(traco_preenchido)
                forma.set_stroke(cor_traco_preenchido)
            else:
                forma.set_fill(False)
                forma.set_stroke(paleta[0])
                forma.set_stroke_weight(traco)
            py5.shape(forma, x, y)
            paleta.rotate(1)

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
    elif key == "r":
        inicializa()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
