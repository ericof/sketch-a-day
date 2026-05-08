"""2026-05-08
Counting 02 (Chaos 01)
Grade com polígonos regulares a partir de 3 lados.
ericof.com|https://ericof.com/en/sketches/2023-11-06
png
Sketch,py5,CreativeCoding,Poligonos
"""

from random import shuffle
from sketches.utils.draw import canvas
from sketches.utils.draw.formas import _gera_forma
from sketches.utils.draw.grade import cria_grade
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

celula_x = 200
m_celula_x = celula_x / 2
celula_y = 200
m_celula_y = celula_y / 2

GRADE = cria_grade(*helpers.DIMENSOES.internal, 0, 0, celula_x, celula_y, False)
FORMAS: dict[int, py5.Py5Shape] = {}
ORDEM: list[int] = []
total_celulas = len(GRADE)
lado_min = 3
lado_max = lado_min + total_celulas
mult = 0.75


def calcula_cor(lado: int, total_células: int) -> list[int]:
    """Gera ``lado`` variações da mesma cor base, alterando S e B.

    A cor base é derivada do número de lados via módulos coprimos,
    garantindo distribuição diversa em faixa cromática vibrante
    (sem extremos brancos ou pretos):

    - ``h = (lado · passo) mod 360`` com ``passo = 360 /
      total_células`` — matiz adapta-se ao tamanho da grade,
      percorrendo o círculo cromático ao longo das células;
    - ``s_base = 60 + (lado · 7) mod 41`` — saturação base em
      ``[60, 100]``;
    - ``b_base = 50 + (lado · 11) mod 41`` — brilho base em
      ``[50, 90]``.

    Os multiplicadores 7 e 11 e o módulo 41 são coprimos entre si,
    evitando bandas onde saturação e brilho coincidam ciclicamente.

    Para cada índice ``i`` em ``[0, lado)``, S e B recebem um
    deslocamento normalizado por ``lado`` (``delta_norm = (i -
    (lado-1)/2) / lado``, sempre em ``[-0.5, +0.5]``), com ganho
    ``±15`` em S e ``∓10`` em B — produzindo o mesmo "spread"
    visual independentemente do número de lados. O resultado é uma
    sequência monocromática progressiva, adequada para aplicar como
    ``set_fills`` em um shape de ``lado`` vértices.

    :param lado: número de lados do polígono (também o tamanho da
        lista retornada).
    :param total_células: número total de células na grade; define
        o passo angular ``360 / total_células`` da distribuição de
        matiz.
    :returns: lista de ``lado`` valores ``py5.color`` com matiz
        comum e variações progressivas de saturação e brilho.
    """
    passo = 360 / total_células
    h = (lado * passo) % 360
    s_base = 60 + (lado * 7) % 41
    b_base = 50 + (lado * 11) % 41
    cores: list[int] = []
    for i in range(lado):
        delta_norm = (i - (lado - 1) / 2) / lado
        s = s_base + delta_norm * 30
        b = b_base - delta_norm * 20
        cores.append(py5.color(h, s, b))
    return cores


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.rect_mode(py5.CORNERS)
    py5.shape_mode(py5.CORNERS)
    py5.color_mode(py5.HSB, 360, 100, 100)
    for lados in range(lado_min, lado_max):
        forma = _gera_forma(lados)
        rotacao = float(py5.radians(360 / lados / 2))
        forma.set_fills(calcula_cor(lados, total_celulas))
        forma.set_stroke("#FFFFFF")
        forma.set_stroke_weight(4)
        forma.rotate(rotacao)
        FORMAS[lados] = forma
    chaves = list(FORMAS.keys())
    shuffle(chaves)
    ORDEM.extend(chaves)


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno)
        for idx, (x, y) in enumerate(GRADE):
            xb, yb = x, y
            with py5.push():
                py5.no_fill()
                py5.stroke("#FFFFFF")
                py5.stroke_weight(3)
                py5.rect(x, y, x + celula_x, y + celula_y)
            chave = ORDEM[idx]
            forma = FORMAS[chave]
            x += m_celula_x
            y += m_celula_y / 4
            py5.shape(forma, x, y, x + celula_x * mult, y + celula_y * mult)
            with py5.push():
                py5.fill("#FFFFFF")
                py5.text_size(15)
                py5.text_align(py5.CORNER, py5.CORNER)
                py5.text(f"{chave}", xb + 5, yb + 5 + m_celula_y / 4)
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
