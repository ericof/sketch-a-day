"""2024-01-28
Genuary 28 - Skeuomorphism.
Um relógio de ponteiros com numerais em romano.
png
Sketch,py5,CreativeCoding,genuary,genuary28
"""
from datetime import datetime, time

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


INICIAL = datetime(2024, 1, 28, 13, 22, 1)


BRACOS = [
    ("hour", 12, 10, 0.7),
    ("minute", 60, 5, 0.9),
    ("second", 60, 4, 0.9),
]

MOLDURA = [
    (610, 2, (360, 0, 100)),
    (600, 5, (360, 0, 70)),
]

NUMEROS = [
    "XII",
    "I",
    "II",
    "III",
    "IIII",
    "V",
    "VI",
    "VII",
    "VIII",
    "VIIII",
    "X",
    "XI",
]


def desenha_braco(comprimento: float, angulo: float = 0.0, espessura: int = 2):
    """Desenha linha a partir de 0,0."""
    x0, y0 = 0, 0
    x1 = py5.cos(py5.radians(angulo)) * comprimento
    y1 = py5.sin(py5.radians(angulo)) * comprimento
    with py5.push_style():
        py5.fill(360, 0, 100)
        py5.stroke(360, 0, 100)
        py5.stroke_weight(espessura)
        py5.line(x0, y0, x1, y1)


def desenha_bracos(raio: int, horario: time):
    with py5.push_matrix():
        py5.translate(py5.width / 2, py5.height / 2, -10)
        for attr, maximo, espessura, fator in BRACOS:
            valor = getattr(horario, attr) % maximo
            angulo = py5.remap(valor, 0, maximo, 0, 360) - 90
            comprimento = raio * fator
            desenha_braco(comprimento, angulo, espessura)


def desenha_moldura():
    with py5.push_matrix():
        py5.translate(py5.width / 2, py5.height / 2, 10)
        py5.fill(360, 80, 80)
        py5.circle(0, 0, 20)
        with py5.push_style():
            py5.fill(360, 0, 80)
            for r, espessura, cor in MOLDURA:
                py5.no_fill()
                py5.stroke(*cor)
                py5.stroke_weight(espessura)
                py5.circle(0, 0, r)
    with py5.push_matrix():
        py5.translate(py5.width / 2, py5.height / 2, -20)
        with py5.push_style():
            py5.no_stroke()
            py5.fill(80)
            py5.circle(0, 0, r - 1)


def desenha_numeros(raio: int):
    with py5.push_matrix():
        py5.translate(py5.width / 2, py5.height / 2, 10)
        with py5.push_style():
            py5.text_font(FONTE)
            for idx, numero in enumerate(NUMEROS):
                angulo = idx * 30 - 90
                x = py5.cos(py5.radians(angulo)) * raio
                y = py5.sin(py5.radians(angulo)) * raio
                py5.fill(360, 0, 100)
                py5.text_size(10)
                py5.text_align(py5.CENTER)
                py5.text(numero, x, y)


def setup():
    global TEMPO_BASE, FONTE
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.frame_rate(1)
    TEMPO_BASE = datetime.now()
    FONTE = py5.create_font("KonamiWaiWaiWorldFamicomExtended", 25)


def draw():
    agora = datetime.now()
    diff = agora - TEMPO_BASE
    horario = INICIAL + diff
    py5.background(0)
    helpers.write_legend(sketch=sketch)
    desenha_moldura()
    desenha_numeros(250)
    desenha_bracos(250, horario)


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
