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


def criar_mascara_furo(
    formato_furo: py5.Py5Shape,
    x_inicial: float,
    y_inicial: float,
    x_final: float,
    y_final: float,
) -> py5.Py5Shape:
    """Cria uma forma vazada, onde formato_furo define o buraco interno.

    Parâmetros:
    - formato_furo: um py5.Shape já existente que será usado como furo
                    (deve conter apenas vértices simples).
    - raio_externo: raio do círculo externo do donut, centrado na tela.

    Retorna:
    - Um novo py5.Shape com um buraco interno definido por formato_furo.
    """
    forma = py5.create_shape()
    forma_interna = (
        formato_furo
        if formato_furo.get_child_count() == 0
        else formato_furo.get_child(0)
    )
    with forma.begin_closed_shape():
        # Retângulo externo (sentido anti-horário)
        forma.vertex(x_inicial, y_inicial)
        forma.vertex(x_final, y_inicial)
        forma.vertex(x_final, y_final)
        forma.vertex(x_inicial, y_final)
        # Contorno interno (o furo) - sentido horário
        with forma.begin_contour():
            for i in reversed(range(forma_interna.get_vertex_count())):
                x, y, _ = forma_interna.get_vertex(i)
                forma.vertex(x, y)
    return forma
