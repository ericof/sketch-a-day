"""2026-03-23
Esfera de Retalhos 04
Esfera formada por folhas orgânicas de cores diversas
ericof.com
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from dataclasses import dataclass
from random import shuffle
from sketches.utils.draw import canvas
from sketches.utils.draw.cores import lerp_color_rgba
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.cores.paletas import lista_paletas
from sketches.utils.helpers import sketches as helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

z_factor = 0.04

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


def gera_espiral(raio: float, num_pontos: int, delta_theta: float = 0.0) -> np.ndarray:
    """Gera pontos de uma espiral Fibonacci na superfície da esfera.

    :param raio: raio da esfera
    :param num_pontos: número de pontos (controla o número de voltas)
    :param delta_theta: deslocamento angular em radianos (para criar bordas paralelas)
    :return: array (N, 3) com coordenadas na superfície da esfera
    """
    indices = np.arange(num_pontos)
    angulo_dourado = np.pi * (3.0 - np.sqrt(5.0))
    y = 1.0 - (2.0 * indices) / (num_pontos - 1)
    raio_xy = np.sqrt(np.maximum(0.0, 1.0 - y * y))
    theta = angulo_dourado * indices + delta_theta
    x = np.cos(theta) * raio_xy
    z = np.sin(theta) * raio_xy
    return np.stack((x, y, z), axis=-1) * raio


def _adiciona_vertice(
    forma: py5.Py5Shape,
    x,
    y,
    z,
    paletas_forma: dict[str, deque[int]],
    cores: dict[str, list[int]],
):
    forma.curve_vertex(x, y, z)
    key = "preenchimento"
    cor = paletas_forma[key][0]
    cores[key].append(cor)
    borda = lerp_color_rgba(cor, py5.color("#000"), t=0.95)
    cores["borda"].append(borda)
    paletas_forma[key].rotate()


def criar_forma(
    raio: float,
    num_pontos: int,
    paletas_forma: dict[str, deque[int]],
    delta_theta: float = 0.08,
) -> py5.Py5Shape:
    """Cria uma fita em espiral sobre a esfera, do polo N ao polo S.

    Duas espirais Fibonacci com mesmo y mas offset angular ±delta_theta
    formam os dois bordos da fita — ambos sempre na superfície da esfera.
    Nos polos, onde raio_xy → 0, os dois bordos convergem naturalmente.

    :param delta_theta: meia-largura angular da fita em radianos.
        Para garantir gap visível, use delta_theta < π / num_voltas,
        onde num_voltas ≈ num_pontos * angulo_dourado / (2π).
    """
    borda1 = gera_espiral(raio, num_pontos, +delta_theta)
    borda2 = gera_espiral(raio, num_pontos, -delta_theta)

    # fita fechada: borda1 polo N→S + borda2 polo S→N
    vertices = np.concatenate([borda1, borda2[::-1]])

    cores: dict[str, list[int]] = {
        "preenchimento": [],
        "borda": [],
    }

    forma = py5.create_shape()
    with forma.begin_closed_shape():
        x, y, z = vertices[-1]
        _adiciona_vertice(forma, x, y, z, paletas_forma, cores)
        for x, y, z in vertices:
            _adiciona_vertice(forma, x, y, z, paletas_forma, cores)
        x, y, z = vertices[-1]
        _adiciona_vertice(forma, x, y, z, paletas_forma, cores)
    forma.set_strokes(cores["borda"])
    forma.set_fills(cores["preenchimento"])
    return forma


def inicializa():
    global forma
    local_paletas = paletas[:]
    shuffle(local_paletas)
    paletas_forma = {
        "preenchimento": local_paletas[0],
    }
    forma = criar_forma(800, 60, paletas_forma, delta_theta=0.2)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    inicializa()


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, rotacao.dist_z)
        py5.rotate_y(py5.radians(rotacao.y))
        py5.rotate_x(py5.radians(rotacao.x))
        py5.rotate_z(py5.radians(rotacao.z))
        py5.shape(forma)

    # Créditos e encerramento
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
        case "r":
            inicializa()
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
