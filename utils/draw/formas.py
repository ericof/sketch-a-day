import numpy as np
import py5


def _gera_forma(lados: int = 3) -> py5.Py5Shape:
    pontos = []
    x, y = 0, 0
    largura = 1
    passo = 360 // lados
    for angulo in range(0, 360, passo):
        x += np.cos(py5.radians(angulo)) * largura
        y += np.sin(py5.radians(angulo)) * largura
        pontos.append((x, y))
    forma = py5.create_shape()
    with forma.begin_closed_shape():
        for x, y in pontos:
            forma.vertex(x, y)
    return forma


def gera_hexagono() -> py5.Py5Shape:
    forma = _gera_forma(6)
    forma.rotate(py5.radians(30))
    return forma


def gera_octagono() -> py5.Py5Shape:
    forma = _gera_forma(8)
    forma.rotate(py5.radians(45))
    return forma
