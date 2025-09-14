"""2025-09-14
Concêntricos
Círculos concêntricos
ericof.com
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

RAIO = 320
TRACO_CIRCULO = 15
TRACO = 5
CENTRO = -40
SEGMENTOS = 10
PALETA = None
PASSO = 20


def desenha_circunferencia(
    cx: float,
    cy: float,
    raio: float,
    traco: int,
    segmentos: int,
    paleta: list[py5.Py5Color],
):
    """Desenha uma circunferência completa usando n segmentos de arco consecutivos."""
    diametro = raio * 2
    with py5.push():
        py5.no_fill()
        py5.stroke_weight(traco)
        py5.stroke_cap(py5.SQUARE)

        arc_span = py5.TWO_PI / segmentos
        for i in range(segmentos):
            cor = paleta[i]
            py5.stroke(cor)
            start_angle = i * arc_span
            end_angle = start_angle + (arc_span * 0.95)
            py5.arc(cx, cy, diametro, diametro, start_angle, end_angle)


def paleta():
    paleta = gera_paleta("pastel", True)
    return paleta


def setup():
    global PALETA, LINKS
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    PALETA = paleta()
    desenha()


def desenha():
    cor_fundo = py5.color(0)
    centro = helpers.DIMENSOES.centro
    paleta = PALETA
    with py5.push():
        py5.translate(*centro, 0)
        py5.rotate(py5.radians(-90))
        for raio in (RAIO // 8, RAIO // 2, RAIO):
            peso = 4
            for z in range(-15, -800, -15):
                with py5.push():
                    py5.translate(0, 0, z)
                    desenha_circunferencia(
                        0,
                        0,
                        raio + (TRACO_CIRCULO * 4),
                        TRACO_CIRCULO,
                        SEGMENTOS,
                        paleta,
                    )
                    py5.no_fill()
                    py5.stroke(py5.color(0))
                    py5.stroke_weight(peso)
                    py5.circle(0, 0, (raio + (TRACO_CIRCULO * 4)) * 2)
                    peso += 0.50
            paleta.rotate(2)

    # Credits and go
    canvas.sketch_frame(
        sketch, cor_fundo, "large_transparent_white", "transparent_white"
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
