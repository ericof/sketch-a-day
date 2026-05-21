"""2026-05-21
Crescimento 09
Grade com círculos concêntricos que nascem a partir do centro e de extremidades.
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
QUADRADO = 150
num_circulos_por_celula = 4

CORES = [
    gera_paleta("Navy-Orange", False),
    gera_paleta("mondrian", False),
]

POS = [
    (QUADRADO / 2, QUADRADO / 2),
    (QUADRADO / 2, 0),
    (0, QUADRADO / 2),
    (QUADRADO, QUADRADO / 2),
    (QUADRADO / 2, QUADRADO),
]


def calcula_grade():
    """Popula ``GRADE`` com buffers e parâmetros de círculos por célula.

    Para cada célula da grade interna: um buffer ``Py5Graphics`` de
    ``QUADRADO`` x ``QUADRADO`` e uma paleta sorteada em ``CORES``
    (cada elemento de ``CORES`` é uma paleta retornada por
    :func:`gera_paleta`). A célula recebe ``num_circulos_por_celula``
    grupos de círculos; cada grupo sorteia sua origem em ``POS``
    (centro da célula + 4 pontos médios das bordas) e contém 10 a 20
    círculos concêntricos compartilhando essa origem, com tamanho (2
    a ``QUADRADO``), cor (sorteada da paleta da célula) e traço (1 a
    3). Um ``passo`` angular é sorteado a cada círculo mas só o do
    último (último grupo, último círculo) é armazenado por célula —
    esse valor modula a fase da animação em :func:`draw` via
    ``i * passo``.
    """
    grade = cria_grade(*helpers.DIMENSOES.internal, 0, 0, celula_x, celula_y, False)
    for x, y in grade:
        cores = py5.random_choice(CORES)
        pg = py5.create_graphics(QUADRADO, QUADRADO)
        fundo = py5.color(4, 5, 5)
        circulos = []
        for _ in range(num_circulos_por_celula):
            num_circulos = py5.random_int(10, 20)
            pos = py5.random_choice(POS)
            for _ in range(num_circulos):
                tamanho = py5.random_int(2, QUADRADO)
                passo = py5.TWO_PI / py5.random_int(2, 22)
                cor = py5.color(py5.random_choice(cores))
                traco = py5.random_int(1, 3)
                circulos.append((pos, tamanho, cor, traco))
        GRADE.append((pg, (x, y), fundo, passo, circulos))


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.RGB)
    calcula_grade()


def draw():
    py5.background(cor_fundo)
    f = py5.frame_count
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, -10)
        for i, (pg, (x, y), fundo, passo, circulos) in enumerate(GRADE):
            with pg.begin_draw():
                pg.background(fundo)
                for circulo in circulos:
                    (xc, yc), d, cor, traco = circulo
                    s = py5.cos(py5.radians(f * 2) + i * passo)
                    d += 65 * s
                    pg.no_fill()
                    pg.stroke(cor)
                    pg.stroke_weight(traco)
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
