"""2024-08-25
Concêntrico 9
Exercício de criação de sketch baseado em formas geométricas concêntricas
png
Sketch,py5,CreativeCoding,Geometry
"""

import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

FUNDO = (180, 80, 80)


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
    py5.blend_mode(py5.BLEND)
    h = 220
    s = 40
    b = 100
    with py5.push_matrix():
        py5.translate(py5.width // 2, py5.height // 2)
        lados = 7
        tamanhos = list(range(1220, 20, -10))
        total = len(tamanhos)
        rot = 0
        forma = poligono(pontos, lados)
        for idx, tamanho in enumerate(tamanhos):
            mult = 1 - (idx / (total * 1.4))
            cor_pintura = py5.color(h * mult, s, b * mult)
            forma.set_fill(cor_pintura)
            forma.set_stroke(cor_pintura)
            py5.shape(forma, 0, 0, tamanho, tamanho)
            forma.rotate(py5.radians(rot))
            rot -= 3

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
