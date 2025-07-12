import numpy as np
import py5


def vertices_poligono_regular(
    largura: float, altura: float, lados: int, rotacao: float = 0.0
) -> np.ndarray:
    """Calcula os vértices de um polígono regular centralizado em uma área de
       largura x altura.

    Parâmetros:
        largura: Largura da área onde o polígono será desenhado.
        altura: Altura da área onde o polígono será desenhado.
        lados: Número de lados do polígono (mínimo 3).
        rotacao: Ângulo de rotação em radianos (padrão 0.0).
                 Use np.pi / lados para orientação com vértice voltado para cima.

    Retorno:
        Um array NumPy de forma (lados, 2) com as coordenadas (x, y) de cada vértice.
    """
    if lados < 3:
        raise ValueError("O polígono deve ter pelo menos 3 lados.")

    # Cálculo do raio máximo para caber na área disponível
    raio_max = min(largura / 2, altura / np.cos(np.pi / lados))

    # Centro do polígono
    centro_x = largura / 2
    centro_y = altura / 2

    # Ângulos de cada vértice
    angulos = np.linspace(0, 2 * np.pi, lados, endpoint=False) + rotacao

    # Cálculo das coordenadas
    coordenadas_x = centro_x + raio_max * np.cos(angulos)
    coordenadas_y = centro_y + raio_max * np.sin(angulos)

    return np.column_stack((coordenadas_x, coordenadas_y))


def gera_poligono_regular(
    lados: int = 3, largura: float = 100, altura: float = 100, rotacao: float = 0.0
) -> py5.Py5Shape:
    """Gera um polígono regular com o número de lados especificado."""
    vertices = vertices_poligono_regular(largura, altura, lados, rotacao)
    forma = py5.create_shape()
    with forma.begin_closed_shape():
        for x, y in vertices:
            forma.vertex(x, y)
    return forma
