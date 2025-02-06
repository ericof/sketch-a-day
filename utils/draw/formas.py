import numpy as np
import py5


def gera_hexagono() -> py5.Py5Shape:
    pontos = []
    x, y = 0, 0
    largura = 1
    for angle in range(0, 360, 60):
        x += np.cos(py5.radians(angle)) * largura
        y += np.sin(py5.radians(angle)) * largura
        pontos.append((x, y))
    forma = py5.create_shape()
    with forma.begin_closed_shape():
        for x, y in pontos:
            forma.vertex(x, y)
    forma.rotate(py5.radians(30))
    return forma
