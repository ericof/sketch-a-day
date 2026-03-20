"""2026-03-20
Esfera de Retalhos 01
Esfera formada por folhas orgânicas de cores diversas
ericof.com
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from dataclasses import dataclass
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.cores.paletas import lista_paletas
from sketches.utils.draw.esfera import pontos_esfera
from sketches.utils.draw.esfera import vizinhos_knn_esfera
from sketches.utils.helpers import sketches as helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

z_factor = 0.02
num_vizinhos = 10

paletas = [
    gera_paleta(name, True) for name in lista_paletas() if name.startswith("op-")
]


@dataclass
class EsferaRotacao:
    x: float = -15
    y: float = 45
    z: float = 0
    dist_z: float = -2000


rotacao = EsferaRotacao()


@dataclass
class PontoEsfera:
    x: float
    y: float
    z: float
    vizinhos: list[tuple[float, float, float]]


esfera: list[PontoEsfera] = []


def calcula_coordenadas(xb: float, yb: float, zb: float) -> tuple[float, float, float]:
    mult = py5.random(1 - z_factor, 1 + z_factor)
    return xb, yb, zb * mult


def bagunca_pontos(pontos: tuple[tuple[float, float, float], ...]):
    """Leve bagunçada nos pontos de uma esfera."""
    resultado = []
    for xb, yb, zb in pontos:
        resultado.append(calcula_coordenadas(xb, yb, zb))
    return np.array(resultado)


def criar_forma(esfera, local_paletas) -> py5.Py5Shape:
    """Cria a forma composta por folhas orgânicas sobre a esfera."""
    forma = py5.create_shape(py5.GROUP)
    for ponto in esfera:
        paleta = local_paletas[0]
        cores = []
        for _ in ponto.vizinhos:
            cores.append(paleta[0])
            paleta.rotate()

        # curve_vertex exige pontos de controle fantasma no início e fim
        # para fechar o contorno suavemente
        cores_ext = [cores[-1], *cores, cores[0]]

        folha = py5.create_shape()
        vizinhos_list = list(ponto.vizinhos)
        with folha.begin_closed_shape():
            folha.curve_vertex(*vizinhos_list[-1])  # ponto de controle fantasma inicial
            for x, y, z in vizinhos_list:
                folha.curve_vertex(x, y, z)
            folha.curve_vertex(*vizinhos_list[0])  # fecha o laço suavemente
        folha.set_strokes(cores_ext)
        folha.set_fills(cores_ext[::-1])
        forma.add_child(folha)
        local_paletas.rotate()
    return forma


def setup():
    global forma
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    pontos = bagunca_pontos(pontos_esfera(800, 200))
    for idx, (x, y, z) in enumerate(pontos):
        vizinhos = [
            tuple(pontos[i]) for i in vizinhos_knn_esfera(pontos, idx, num_vizinhos)
        ]
        esfera.append(PontoEsfera(x, y, z, vizinhos))
    local_paletas = deque(paletas[:])
    forma = criar_forma(esfera, local_paletas)


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, rotacao.dist_z)
        py5.rotate_y(py5.radians(rotacao.y))
        py5.rotate_x(py5.radians(rotacao.x))
        py5.rotate_z(py5.radians(rotacao.z))
        py5.shape(forma)

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
    match py5.key:
        case " ":
            save_and_close()
        case "+":
            rotacao.dist_z += 50
        case "-":
            rotacao.dist_z -= 50
    match py5.key_code:
        case py5.UP:
            rotacao.x += 3
        case py5.DOWN:
            rotacao.x -= 3
        case py5.LEFT:
            rotacao.y += 3
        case py5.RIGHT:
            rotacao.y -= 3
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
