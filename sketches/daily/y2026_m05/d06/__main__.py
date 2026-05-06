"""2026-05-06
MaySiXth (MSX Day)
Lembranças dos tempos de MSX
ericof.com|https://paulwratt.github.io/programmers-palettes/HW-MSX/HW-MSX-palettes.html
png
Sketch,py5,CreativeCoding,MaySiXth
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.grade import cria_grade
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
paleta = gera_paleta("msx1", False)


def estrela(r: float = 200, ri: float = 180) -> py5.Py5Shape:
    """Cria uma estrela de 5 pontas centrada na origem.

    Gera o shape alternando vértices externos (raio ``r``) e internos
    (raio ``ri``) ao longo de 5 passos de ``an = 2·pi/5``. O shape fica
    em coordenadas locais — a translação é responsabilidade de quem
    desenha via :func:`py5.shape`. Cada iteração emite o vértice
    externo no ângulo ``a`` seguido do interno em ``a + an/2``; o
    shape fechado conecta o último ponto ao primeiro, formando 10
    vértices (5 pontas + 5 reentrâncias).

    :param r: raio externo da estrela em pixels.
    :param ri: raio interno da estrela em pixels.
    :returns: ``Py5Shape`` fechado pronto para ser desenhado.
    """
    an = py5.PI * 2 / 5
    a = 0
    forma = py5.create_shape()
    with forma.begin_closed_shape():
        while a < py5.PI * 2 - 0.1:
            x0 = r * py5.cos(a)
            y0 = r * py5.sin(a) * -1
            x2 = ri * py5.cos(a + an / 2)
            y2 = ri * py5.sin(a + an / 2) * -1
            forma.vertices([
                [x0, y0],
                [x2, y2],
            ])
            a += an
    return forma


def cria_estrelas() -> list[tuple[float, float, py5.Py5Shape, float, int, int]]:
    """Monta a lista de estrelas posicionadas numa grade alternada.

    Para cada célula de uma grade alternada de ``80x80`` pixels que
    cobre o canvas externo, sorteia:

    - ``cor`` e ``traco`` da paleta MSX1 (com os dois tons de preto
      iniciais já removidos via slice ``[2:]``), garantindo via
      reamostragem que sejam **diferentes** — caso contrário o
      contorno desapareceria.
    - ``angulo`` em **graus** via Gaussiana ``mu=0, sigma=60``,
      convertido para radianos antes de aplicar em ``forma.rotate``.
    - ``ri`` (raio interno) com pequeno jitter Gaussiano em torno de
      ``r/2`` (``sigma=5%``), variando o "estilo" de cada estrela.

    :returns: lista de tuplas ``(x, y, forma, ri, traco, cor)`` para
        cada estrela posicionada.
    """
    celula_x = 80
    celula_y = 80
    r = celula_x * 0.5
    estrelas = []
    paleta_msx = paleta[2:]
    for x, y in cria_grade(*helpers.DIMENSOES.external, 0, 0, celula_x, celula_y, True):
        cor = py5.color(py5.random_choice(paleta_msx))
        traco = py5.color(py5.random_choice(paleta_msx))
        while traco == cor:
            traco = py5.color(py5.random_choice(paleta_msx))
        angulo = py5.random_gaussian(0, 60)
        ri = r * py5.random_gaussian(0.5, 0.05)
        forma = estrela(r, ri)
        forma.rotate(py5.radians(angulo))
        estrelas.append((x, y, forma, ri, traco, cor))
    return estrelas


def setup():
    global estrelas
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.shape_mode(py5.CORNER)
    estrelas = cria_estrelas()


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno)
        for x, y, forma, ri, traco, cor in estrelas:
            forma.set_stroke(traco)
            forma.set_fill(cor)
            py5.shape(forma, x, y)
            with py5.push():
                py5.stroke("#000")
                py5.stroke_weight(ri / 2)
                py5.point(x, y)
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
