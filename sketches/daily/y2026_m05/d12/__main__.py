"""2026-05-12
Crescimento 01
Grade com círculos concêntricos que nascem a partir de um dos cantos
ericof.com|https://ericof.com/en/sketches/2024-07-30
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.grade import cria_grade
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

GRADE = []
celula_x = 100
celula_y = 100
QUADRADO = 96

CORES = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
]

POS = [
    (QUADRADO, 0),
    (0, QUADRADO),
    (QUADRADO, QUADRADO),
    (0, 0),
]


def calcula_grade():
    """Popula ``GRADE`` com buffers e parâmetros de círculos por célula.

    Para cada célula da grade interna: um buffer ``Py5Graphics`` de
    ``QUADRADO`` x ``QUADRADO``, um canto compartilhado (sorteado de
    ``POS``), e 10 a 20 círculos concêntricos com tamanho, cor (de
    ``CORES``) e passo angular aleatórios. O ``passo`` armazenado por
    célula é o do último círculo gerado e modula a fase da animação em
    :func:`draw`.
    """
    grade = cria_grade(*helpers.DIMENSOES.internal, 0, 0, celula_x, celula_y, False)
    for x, y in grade:
        pg = py5.create_graphics(QUADRADO, QUADRADO)
        fundo = (240, 233, 211)
        num_circulos = py5.random_int(10, 20)
        circulos = []
        pos = py5.random_choice(POS)
        for _ in range(num_circulos):
            tamanho = py5.random_int(2, QUADRADO)
            passo = py5.TWO_PI / py5.random_int(2, 22)
            cor = py5.random_choice(CORES)
            circulos.append((pos, tamanho, cor))
        GRADE.append((pg, (x, y), fundo, passo, circulos))


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    calcula_grade()


def draw():
    py5.background(cor_fundo)
    f = py5.frame_count
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, -10)
        for i, (pg, (x, y), fundo, passo, circulos) in enumerate(GRADE):
            with pg.begin_draw():
                pg.background(*fundo)
                for circulo in circulos:
                    (xc, yc), d, cor = circulo
                    s = py5.cos(py5.radians(f * 2) + i * passo)
                    d += 65 * s
                    pg.no_fill()
                    pg.stroke(*cor)
                    pg.circle(xc, yc, d)
            py5.image(pg, x, y)
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
