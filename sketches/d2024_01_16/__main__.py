"""2024-01-16
Genuary 16 - Draw 10 000 of something.
Dez mil retângulos de diferentes cores.
png
Sketch,py5,CreativeCoding,genuary,genuary16
"""
from random import shuffle

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def sorteia_pontos(i=0, f=800, items=20):
    pontos = []
    todos = list(range(i, f))
    shuffle(todos)
    sorteio = {i, f}
    while len(sorteio) <= items:
        sorteio.add(todos.pop())
    sorteio = sorted(list(sorteio))
    for idx, pi in enumerate(sorteio[:-1]):
        pf = sorteio[idx + 1]
        pontos.append((pi, pf))
    return pontos


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CORNERS)
    py5.no_stroke()
    contador = 0
    linhas = 40
    y = sorteia_pontos(20, 720, linhas)
    for linha, (y0, y1) in enumerate(y):
        x = sorteia_pontos(10, 790, 25)
        for x0, x1 in x:
            hb = (linha / linhas) * 300
            h = py5.remap(py5.sin(x0 * y0), -1, 1, hb, hb + 30)
            s = py5.random_int(80, 100) + x0 % 100
            b = py5.remap(x0 - y0, -800, 800, 50, 90)
            contador += 1
            cor = py5.color(h, s, b)
            py5.fill(cor)
            py5.stroke("#ccc")
            py5.stroke_weight(1)
            py5.rect(x0, y0, x1, y1)
    helpers.write_legend(sketch=sketch)


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
