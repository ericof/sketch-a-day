"""2024-08-19
Concêntrico 3
Exercício de criação de sketch baseado em formas geométricas concêntricas
png
Sketch,py5,CreativeCoding,Geometry
"""

import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

FUNDO = (46, 12, 98)


def calcula_circulo(diametro: int) -> list[tuple[int, int]]:
    pontos = []
    raio = diametro // 2
    n = 360
    for ponto in range(0, n + 1):
        x = np.cos(2 * py5.PI / n * ponto) * raio
        y = np.sin(2 * py5.PI / n * ponto) * raio
        pontos.append((int(x), int(y)))
    return pontos


def poligono(pontos: list[tuple[int, int]], lados=3) -> py5.Py5Shape:
    angulo = 360 / lados
    s = py5.create_shape()
    with s.begin_closed_shape():
        for i in range(0, lados + 1):
            if (idx := int(i * angulo)) > 360:
                idx = idx % 360
            x, y = pontos[idx]
            s.vertex(x, y)
    return s


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(*FUNDO)
    pontos = calcula_circulo(800)
    py5.shape_mode(py5.CORNERS)
    h = 126
    s = 12
    b = 97
    with py5.push_matrix():
        py5.translate(py5.width // 2, py5.height // 2)
        lados = 14
        tamanhos = list(range(1120, 20, -20))
        total = len(tamanhos)
        for idx, tamanho in enumerate(tamanhos):
            if not idx % 9:
                lados -= 1
                rot = 0
            forma = poligono(pontos, lados)
            mult = 1 - (idx / total)
            resto = idx % 3
            if not idx % 3:
                cor_traco = cor_pintura = py5.color(*FUNDO)
            else:
                cor_traco = py5.color(h, s, 80)
                cor_pintura = py5.color(h, s, b * mult)
            forma.set_stroke_weight(resto + 1)
            forma.set_stroke(cor_traco)
            forma.set_fill(cor_pintura)
            py5.shape(forma, 0, 0, tamanho, tamanho)
            forma.rotate(py5.radians(rot))
            if lados % 2 == 1:
                rot += 15
            else:
                rot -= 15

    helpers.write_legend(sketch=sketch, frame="#000")


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
