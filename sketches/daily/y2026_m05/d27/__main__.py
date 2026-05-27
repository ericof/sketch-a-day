"""2026-05-27
Crescimento 15
Grade com círculos concêntricos
ericof.com|https://ericof.com/en/sketches/2024-07-30
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

GRADE = []
celula_x = 160
celula_y = 160
tamanho_x = 120
num_circulos_por_celula = 1
circ_min = 5
circ_max = 20
traco_min = 1
traco_max = 5

POS = [
    (celula_x / 2, celula_y / 2),
]

CORES = gera_paleta("mondrian", False)


def calcula_grade():
    grade = cria_grade(*helpers.DIMENSOES.internal, 0, 0, celula_x, celula_y, False)
    for x, y in grade:
        fundo = py5.color("#EADDCC")
        circulos = []
        for _ in range(num_circulos_por_celula):
            num_circulos = py5.random_int(circ_min, circ_max)
            pos = py5.random_choice(POS)
            for _ in range(num_circulos):
                tamanho = py5.random_int(2, tamanho_x)
                passo = py5.TWO_PI / py5.random_int(2, 22)
                cor = py5.color(py5.random_choice(CORES))
                traco = py5.random_int(traco_min, traco_max)
                circulos.append((pos, tamanho, cor, traco))
        GRADE.append(((x, y), fundo, passo, circulos))


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.RGB)
    calcula_grade()


def draw():
    py5.background(cor_fundo)
    f = py5.frame_count
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, -10)
        for i, ((x, y), fundo, passo, circulos) in enumerate(GRADE):
            with py5.push():
                py5.stroke(fundo)
                py5.stroke_weight(4)
                py5.no_fill()
                xi, xf = x, celula_x
                yi, yf = y, y + celula_y
                py5.rect(xi, yi, xf, yf)
            with py5.push():
                py5.translate(x, y, 0)
                for circulo in circulos:
                    (xc, yc), d, cor, traco = circulo
                    s = py5.cos(py5.radians(f * 2) + i * passo)
                    d += 65 * s
                    py5.no_fill()
                    py5.stroke(cor)
                    py5.stroke_weight(traco)
                    py5.circle(xc, yc, d)
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
