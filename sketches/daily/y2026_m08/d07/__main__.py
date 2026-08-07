"""2026-08-07
Acumulando Pontos 01
Usando polígonos regulares, criamos uma circunferência de pontos.
ericof.com|https://ericof.com/en/sketches/2023-09-03
png
Sketch,py5,CreativeCoding
"""

from sketches.padroes.poligonos import vertices_poligono_regular
from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

lados = 8
rotacao = 0.0

pontos_por_frame = 400
fator_atracao = 0.666
peso_ponto = 2
saturacao = (80, 100)
brilho = (80, 100)

vertices: np.ndarray
matizes: np.ndarray
camada: py5.Py5Graphics


def inicializa() -> None:
    """Calcula o polígono da área interna e cria a camada acumuladora.

    Os vértices vêm de :func:`vertices_poligono_regular` em coordenadas locais
    da área interna. O matiz de cada vértice é o seu ângulo (em graus) em
    relação ao centro do polígono.
    """
    global vertices, matizes, camada
    camada = py5.create_graphics(*helpers.DIMENSOES.internal, py5.P3D)
    with camada.begin_draw():
        camada.color_mode(py5.HSB, 360, 100, 100)
        camada.clear()
    largura, altura = camada.width, camada.height
    vertices = vertices_poligono_regular(largura, altura, lados, rotacao)
    deltas = vertices - np.array([largura / 2, altura / 2])
    matizes = np.degrees(np.arctan2(deltas[:, 1], deltas[:, 0])) % 360


def dentro_do_poligono(x: float, y: float) -> bool:
    """Verifica se um ponto está dentro do polígono convexo.

    :param x: Coordenada x, em coordenadas locais da área interna.
    :param y: Coordenada y, em coordenadas locais da área interna.
    :returns: ``True`` se o ponto estiver dentro do polígono.
    """
    arestas = np.roll(vertices, -1, axis=0) - vertices
    para_ponto = np.array([x, y]) - vertices
    cruzados = arestas[:, 0] * para_ponto[:, 1] - arestas[:, 1] * para_ponto[:, 0]
    return bool(np.all(cruzados >= 0) or np.all(cruzados <= 0))


def sorteia_ponto_interno() -> tuple[float, float]:
    """Sorteia um ponto uniforme dentro do polígono, por rejeição na bounding box.

    :returns: Par ``(x, y)`` em coordenadas locais da área interna.
    """
    x_min, y_min = vertices.min(axis=0)
    x_max, y_max = vertices.max(axis=0)
    while True:
        x = py5.random(x_min, x_max)
        y = py5.random(y_min, y_max)
        if dentro_do_poligono(x, y):
            return x, y


def acumula_pontos(quantidade: int) -> None:
    """Desenha na camada pontos atraídos para os vértices do polígono.

    Cada ponto nasce numa posição uniforme dentro do polígono e é deslocado
    ``fator_atracao`` do caminho até um vértice sorteado, herdando o matiz
    desse vértice com saturação e brilho aleatórios.

    :param quantidade: Número de pontos a acrescentar nesta chamada.
    """
    with camada.begin_draw():
        camada.stroke_weight(peso_ponto)
        for _ in range(quantidade):
            x0, y0 = sorteia_ponto_interno()
            idx = py5.random_int(0, lados - 1)
            x1, y1 = vertices[idx]
            cor = camada.color(
                float(matizes[idx]),
                py5.random(*saturacao),
                py5.random(*brilho),
            )
            camada.stroke(cor)
            x = float(py5.lerp(x0, x1, fator_atracao))
            y = float(py5.lerp(y0, y1, fator_atracao))
            camada.point(x, y)


def setup():
    py5.pixel_density(py5.display_density())
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    inicializa()
    acumula_pontos(pontos_por_frame)


def draw():
    py5.background(cor_fundo)
    acumula_pontos(pontos_por_frame)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno)
        if camada is not None:
            largura = helpers.DIMENSOES.internal[0] * py5.display_density()
            altura = helpers.DIMENSOES.internal[1] * py5.display_density()
            py5.image(camada, 0, 0, largura, altura)
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
