"""2026-02-01
Multiple Mondrian 02
Inspirado em Piet Mondrian e suas composições geométricas com retângulos coloridos.
ericof.com|https://openprocessing.org/sketch/2343601
png
Sketch,py5,CreativeCoding
"""

from random import shuffle
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.cores.paletas import lista_paletas
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
retangulos = []

largura, altura = helpers.DIMENSOES.internal

linhas = 10
colunas = 10
perc = 0.95
grade_lar = largura * perc
grade_alt = altura * perc
sep = 5
cel_lar = grade_lar / colunas
cel_alt = grade_alt / linhas
proporcao_ret = 0.75
tam_ret = cel_lar * proporcao_ret
meio_ret = tam_ret / 2

peso = largura * 0.006


def ease_in_out_quint(x: float) -> float:
    return 16 * x**5 if x < 0.5 else 1 - ((-2 * x + 2) ** 5) / 2


class SuperRect:
    def __init__(self, x, y, w, h, a, sep, clr):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.a = a
        self.clr = clr
        self.separate = sep
        self.origin_w = w
        self.origin_h = h

        self.update()
        self.w = self.to_w
        self.h = self.to_h
        self.update()

        self.alterna = False
        self.duracao = 90
        self.tempo = 0

    def move(self):
        if self.alterna:
            self.tempo += 1
            if 0 < self.tempo < self.duracao:
                n = py5.norm(self.tempo, 0, self.duracao)
                e = ease_in_out_quint(n)
                self.w = py5.lerp(self.from_w, self.to_w, e)
                self.h = py5.lerp(self.from_h, self.to_h, e)
            elif self.tempo > self.duracao:
                self.alterna = False

        if (not self.alterna) and (py5.frame_count % 30 == 0) and (py5.random(1) < 0.1):
            self.alterna = True
            self.tempo = 0
            self.update()

    def update(self):
        self.from_w = self.w
        self.to_w = (self.origin_w / self.separate) * int(py5.random(self.separate) + 1)

        self.from_h = self.h
        self.to_h = (self.origin_h / self.separate) * int(py5.random(self.separate) + 1)

        self.tempo = 0


def celula(i, j, sep, paletas) -> list[SuperRect]:
    """Define uma célula da grade com retângulos coloridos."""
    retangulos = []
    paleta = py5.random_choice(paletas)
    x = i * cel_lar + cel_lar / 2
    y = j * cel_alt + cel_alt / 2
    cols_local = paleta[:]
    shuffle(cols_local)

    retangulos.append(
        SuperRect(
            x - (meio_ret),
            y - (meio_ret),
            tam_ret,
            tam_ret,
            0,
            sep,
            cols_local[0],
        )
    )
    retangulos.append(
        SuperRect(
            x + (meio_ret),
            y - (meio_ret),
            tam_ret,
            tam_ret,
            py5.HALF_PI,
            sep,
            cols_local[1],
        )
    )
    retangulos.append(
        SuperRect(
            x + (meio_ret),
            y + (meio_ret),
            tam_ret,
            tam_ret,
            py5.PI,
            sep,
            cols_local[2],
        )
    )
    retangulos.append(
        SuperRect(
            x - (meio_ret),
            y + (meio_ret),
            tam_ret,
            tam_ret,
            py5.PI * 1.5,
            sep,
            cols_local[3],
        )
    )
    return retangulos


def setup():
    global grade_lar, grade_alt, retangulos
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    todas_paletas = [gera_paleta(name) for name in lista_paletas()]
    paletas = [pal for pal in todas_paletas if len(pal) >= 4]

    retangulos = []
    for i in range(colunas):
        for j in range(linhas):
            retangulos.extend(celula(i, j, sep, paletas))
    shuffle(retangulos)


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno)
        with py5.push():
            py5.translate((largura - grade_lar) / 2, (altura - grade_alt) / 2)
            # filled rectangles
            py5.no_stroke()
            for r in retangulos:
                with py5.push():
                    py5.translate(r.x, r.y)
                    py5.rotate(r.a)
                    py5.fill(r.clr)
                    py5.rect(0, 0, r.w, r.h)

            # outlines
            py5.stroke_weight(peso)
            py5.stroke(cor_fundo)
            py5.no_fill()
            for r in retangulos:
                with py5.push():
                    py5.translate(r.x, r.y)
                    py5.rotate(r.a)
                    py5.rect(0, 0, r.w, r.h)

            # animate sizes
            for r in retangulos:
                r.move()
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
