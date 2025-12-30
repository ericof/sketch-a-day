"""2025-12-30
Padrões vetoriais 03
Grade de padrões vetoriais com partículas seguindo um campo vetorial
ericof.com|https://openprocessing.org/sketch/2760720
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers
from typing import cast

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
cor_borda = py5.color(80)
cor_borda_alt = py5.color(255)
paleta = gera_paleta("bright-colors")
particulas = []


def gera_cor():
    return py5.random_choice(paleta)


def campo_vetor(vetor: py5.Py5Vector2D, escala: float) -> py5.Py5Vector2D:
    x = py5.remap(vetor.x, 100, 900, 0, escala)
    y = py5.remap(vetor.y, 100, 900, 0, escala)

    k1 = 5
    k2 = 3

    u = py5.cos(k1 * y) + py5.cos(k2 * y)
    v = py5.sin(k2 * x) - py5.cos(k1 * x)

    novo_vetor = cast(py5.Py5Vector2D, py5.Py5Vector2D(u, v))
    return novo_vetor


class Particula:
    p: py5.Py5Vector2D
    p_old: py5.Py5Vector2D

    def __init__(self, x: float, y: float, grossura: float, escala: float) -> None:
        self.p = cast(py5.Py5Vector2D, py5.Py5Vector2D(x, y))
        self.p_old = cast(py5.Py5Vector2D, py5.Py5Vector2D(self.p.x, self.p.y))
        self.grossura = grossura
        self.velocidade = 1
        self.cor = gera_cor()
        self.direcao = -1
        self.escala = escala

    def update(self):
        self.p.x += self.velocidade * self.direcao * campo_vetor(self.p, self.escala).x
        self.p.y += self.velocidade * self.direcao * campo_vetor(self.p, self.escala).y
        py5.stroke_weight(self.grossura)
        py5.stroke(self.cor)
        py5.line(self.p_old.x, self.p_old.y, self.p.x, self.p.y)
        py5.stroke(self.cor)
        self.p_old = self.p


def desenha_grade():
    py5.stroke(cor_borda)
    py5.stroke_weight(15)

    for x in range(100, 900, 200):
        py5.line(100, x, 900, x)
        py5.line(x, 100, x, 900)

    py5.stroke(cor_borda_alt)
    py5.stroke_weight(5)
    for x in range(100, 900, 200):
        py5.line(100, x, 900, x)
        py5.line(x, 100, x, 900)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.rect_mode(py5.CENTER)
    py5.background(cor_fundo)
    for x in range(100, 901, 25):
        for y in range(100, 901, 25):
            grossura = py5.random_int(5, 15)
            escala = py5.random_int(10, 30)
            particulas.append(Particula(x, y, grossura, escala))


def draw():
    for particula in particulas:
        particula.update()
    desenha_grade()
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro)
        py5.no_fill()
        py5.stroke(cor_borda)
        py5.stroke_weight(15)
        py5.square(0, 0, 800)

    with py5.push():
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
