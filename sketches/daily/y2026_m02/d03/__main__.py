"""2026-02-03
Square Moviment 01
Grade de quadrados que se expandem em direções aleatórias e retornam à posição original.
ericof.com|https://openprocessing.org/sketch/2363803
png
Sketch,py5,CreativeCoding
"""

from random import shuffle
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
objs: list["SuperQuadrado"] = []
GRADE_MULT = 0.95
GRADE_CELULAS = 20
CELULA_MULT = 0.8
paleta = gera_paleta("op-2363803")


def ease_in_out_quint(x):
    return 16 * x**5 if x < 0.5 else 1 - ((-2 * x + 2) ** 5) / 2


class SuperQuadrado:
    """Quadrado que se move a partir de sua posição original."""

    x: float
    y: float
    w: float
    origin_x: float
    origin_y: float
    current_x: float
    current_y: float
    from_x: float
    from_y: float
    xpm: float
    ypm: float
    len: int
    to_x: float
    to_y: float
    time: int
    time_1: int
    time_2: int
    time_3: int
    clr: py5.Py5Color

    def __init__(self, x: float, y: float, w: float, cor: py5.Py5Color):
        self.x = x
        self.y = y
        self.w = w

        self.origin_x = x
        self.origin_y = y

        self.current_x = x
        self.current_y = y

        self.from_x = self.current_x
        self.from_y = self.current_y

        self.xpm = py5.random_choice([-1, 1])
        self.ypm = py5.random_choice([-1, 1])
        self.len = int(py5.random(1, 4))

        self.to_x = self.origin_x + self.w * self.len * self.xpm
        self.to_y = self.origin_y + self.w * self.len * self.ypm

        self.time = -int(py5.random(500))
        self.time_1 = 60
        self.time_2 = self.time_1 + 200
        self.time_3 = self.time_2 + 60

        self.clr = cor

    def show(self):
        py5.no_stroke()
        py5.fill(self.clr)

        meio_w = self.w / 2
        origem_x = self.origin_x
        origem_y = self.origin_y
        atual_x = self.current_x
        atual_y = self.current_y

        with py5.begin_shape(py5.QUADS):
            py5.vertex(origem_x - meio_w, origem_y - meio_w)
            py5.vertex(origem_x + meio_w, origem_y - meio_w)
            py5.vertex(atual_x + meio_w, atual_y - meio_w)
            py5.vertex(atual_x - meio_w, atual_y - meio_w)

            py5.vertex(origem_x + meio_w, origem_y - meio_w)
            py5.vertex(origem_x + meio_w, origem_y + meio_w)
            py5.vertex(atual_x + meio_w, atual_y + meio_w)
            py5.vertex(atual_x + meio_w, atual_y - meio_w)

            py5.vertex(origem_x + meio_w, origem_y + meio_w)
            py5.vertex(origem_x - meio_w, origem_y + meio_w)
            py5.vertex(atual_x - meio_w, atual_y + meio_w)
            py5.vertex(atual_x + meio_w, atual_y + meio_w)

            py5.vertex(origem_x - meio_w, origem_y + meio_w)
            py5.vertex(origem_x - meio_w, origem_y - meio_w)
            py5.vertex(atual_x - meio_w, atual_y - meio_w)
            py5.vertex(atual_x - meio_w, atual_y + meio_w)

            py5.fill(0)
            py5.vertex(atual_x - meio_w, atual_y - meio_w)
            py5.vertex(atual_x + meio_w, atual_y - meio_w)
            py5.vertex(atual_x + meio_w, atual_y + meio_w)
            py5.vertex(atual_x - meio_w, atual_y + meio_w)

        with py5.begin_shape(py5.QUADS):
            if self.ypm == 1:
                py5.fill(0, 75)
                py5.vertex(origem_x - meio_w, origem_y - meio_w)
                py5.vertex(origem_x + meio_w, origem_y - meio_w)
                py5.vertex(atual_x + meio_w, atual_y - meio_w)
                py5.vertex(atual_x - meio_w, atual_y - meio_w)

            if self.xpm == -1:
                py5.fill(0, 150)
                py5.vertex(origem_x + meio_w, origem_y - meio_w)
                py5.vertex(origem_x + meio_w, origem_y + meio_w)
                py5.vertex(atual_x + meio_w, atual_y + meio_w)
                py5.vertex(atual_x + meio_w, atual_y - meio_w)

            if self.ypm == -1:
                py5.fill(255, 150)
                py5.vertex(origem_x + meio_w, origem_y + meio_w)
                py5.vertex(origem_x - meio_w, origem_y + meio_w)
                py5.vertex(atual_x - meio_w, atual_y + meio_w)
                py5.vertex(atual_x + meio_w, atual_y + meio_w)

            if self.xpm == 1:
                py5.fill(255, 75)
                py5.vertex(origem_x - meio_w, origem_y + meio_w)
                py5.vertex(origem_x - meio_w, origem_y - meio_w)
                py5.vertex(atual_x - meio_w, atual_y - meio_w)
                py5.vertex(atual_x - meio_w, atual_y + meio_w)

        py5.fill(self.clr)
        py5.square(self.current_x, self.current_y, self.w)

    def move(self):
        if 0 < self.time < self.time_1:
            n = py5.norm(self.time, 0, self.time_1 - 1)
            t = ease_in_out_quint(n)
            self.current_x = py5.lerp(self.from_x, self.to_x, t)
            self.current_y = py5.lerp(self.from_y, self.to_y, t)

        elif self.time_2 < self.time < self.time_3:
            n = py5.norm(self.time, self.time_2, self.time_3 - 1)
            t = ease_in_out_quint(n)
            self.current_x = py5.lerp(self.to_x, self.from_x, t)
            self.current_y = py5.lerp(self.to_y, self.from_y, t)

        if self.time > self.time_3:
            self.time = -int(py5.random(500))

            self.xpm = py5.random_choice([-1, 1])
            self.ypm = py5.random_choice([-1, 1])
            self.len = int(py5.random(1, 4))
            self.to_x = self.origin_x + self.w * self.len * self.xpm
            self.to_y = self.origin_y + self.w * self.len * self.ypm

        self.time += 1


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CENTER)
    largura, altura = helpers.DIMENSOES.internal
    grade_tam = largura * GRADE_MULT
    celula_tam = grade_tam / GRADE_CELULAS
    celula_metade = celula_tam / 2
    celula_interna_tam = celula_tam * CELULA_MULT

    for i in range(GRADE_CELULAS):
        for j in range(GRADE_CELULAS):
            x = i * celula_tam + celula_metade + ((largura - grade_tam) / 2)
            y = j * celula_tam + celula_metade + ((altura - grade_tam) / 2)
            cor = py5.random_choice(paleta)
            objs.append(SuperQuadrado(x, y, celula_interna_tam, cor))

    shuffle(objs)


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, -10)
        for obj in objs:
            obj.show()
            obj.move()
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
