"""2026-08-27
Interferences 02
Grade com hexágonos, cores e tamanhos diversos.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from sketches.padroes.poligonos import gera_poligono_regular
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.grade import cria_grade_ex
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

margem_x: int = 0
margem_y: int = 0
celula_x: int = 80
celula_y: int = 80
tamanho_max: int = 50
tamanho_passo: int = 5
tamanho_min: int = 10
lados: int = 6
rotacao_inicial: float = (py5.PI / 6) * 1.3

PALETAS: tuple[str, ...] = (
    "op-1726494-01",
    "south-africa",
    "op-1726494-01",
    "pycon-colombia-2025",
)


def inicializa() -> None:
    global forma, grade
    largura, altura = helpers.DIMENSOES.external
    grade = cria_grade_ex(
        largura,
        altura,
        margem_x,
        margem_y,
        celula_x,
        celula_y,
        True,
    )
    forma = gera_poligono_regular(
        lados=lados, largura=celula_x, altura=celula_y, rotacao=rotacao_inicial
    )


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.shape_mode(py5.CENTER)
    inicializa()


def desenha_forma(x: float, y: float, cx: int, cy: int, paleta) -> None:
    with py5.push_matrix():
        py5.translate(x, y)
        for tamanho in range(tamanho_max, tamanho_min - 1, -tamanho_passo):
            py5.stroke(paleta[0])
            forma.set_stroke(paleta[0])
            forma.set_stroke_weight(2)
            forma.set_fill(False)
            py5.shape(forma, tamanho, tamanho)
            paleta.rotate(1)


def draw():
    py5.background(cor_fundo)
    paletas = deque(gera_paleta(paleta, True) for paleta in PALETAS)
    with py5.push_matrix():
        py5.translate(0, 0, -20)
        for cx, x, cy, y in grade:
            paleta = paletas[0]
            desenha_forma(x, y, cx, cy, paleta)
            paletas.rotate(1)
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
