"""2026-03-19
Manchas concêntricas 02
Distribuição de círculos concêntricos
ericof.com
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from dataclasses import dataclass
from sketches.utils.draw import canvas
from sketches.utils.draw.cores import extrai_rgba
from sketches.utils.draw.cores import lerp_color_rgba
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.cores.paletas import lista_paletas
from sketches.utils.helpers import sketches as helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
paletas: deque[list[int]] = deque([
    gera_paleta("op-2363803") for name in lista_paletas() if name.startswith("op-")
])


@dataclass
class CirculoRaio:
    raio: float
    traco: float
    cor: int


@dataclass
class CirculosConcentricos:
    x: float
    y: float
    z: float
    circulos: list[CirculoRaio]


CIRCULOS: list[CirculosConcentricos] = []


def calcula_raios(
    num: int,
    cor_1: int,
    cor_2: int,
    z_dist: float,
    inicial: float,
    final: float,
) -> list[CirculoRaio]:
    """Considerando valores para raio inicial e final, retorna lista com num CirculoRaio

    * Primeiramente calculamos a distância média entre os raios
    * Iteramos por range(num)
        * raio será a distância média + random_int
        * traco será (distância média /2) * random(0.2, 0.75)

    """
    raios = []
    dist_media = (final - inicial) / num
    traco_base = dist_media / 1.2
    t_minmax = (0, num)
    for idx in range(num):
        r, g, b, a = extrai_rgba(lerp_color_rgba(cor_1, cor_2, idx, t_minmax))
        a *= z_dist
        cor = py5.color(r, g, b, a)
        raios.append(
            CirculoRaio(
                raio=(dist_media + py5.random_int(-3, 3)) * idx + inicial,
                cor=cor,
                traco=traco_base * py5.random(0.2, 0.75),
            )
        )
    return raios


def calcula_circulos(
    x: float,
    y: float,
    z: float,
    z_dist: float,
    r_range: tuple[float, float],
    total: int,
    cor_1: int,
    cor_2: int,
) -> CirculosConcentricos:
    circulos = calcula_raios(total, cor_1, cor_2, z_dist, *r_range)
    return CirculosConcentricos(x=x, y=y, z=z, circulos=circulos)


def calcula_pontos(
    total: int,
    x_range: tuple[float, float],
    y_range: tuple[float, float],
    z_range: tuple[float, float],
    coeficiente: int = 6,
) -> tuple[tuple[tuple[float, float, float], ...], tuple[float, float]]:
    """Retorna uma tupla con `total` coordenadas (x, y, z).

    Os pontos são distribuidos, inicialmente em uma matrix 2d de
    maneira equidistante (respeitando os limites estipulados em x_range
    e y_range).
    Para cada ponto, os valores de x e y devem ter aplicado algum `noise`
    para que a distribuição dos pontos seja levemente "bagunçada"
    A coordenada z será calculada utilizando o py5.random(*z_range)
    """
    cols = int(np.ceil(np.sqrt(total)))
    rows = int(np.ceil(total / cols))

    xs = np.linspace(x_range[0], x_range[1], cols)
    ys = np.linspace(y_range[0], y_range[1], rows)
    grid_x, grid_y = np.meshgrid(xs, ys)

    step_x = (x_range[1] - x_range[0]) / cols
    # Desloca meio passo em x nas linhas ímpares
    offset = np.where(np.arange(rows) % 2 == 1, step_x / 2, 0.0)
    grid_x += offset[:, np.newaxis]

    flat_x = grid_x.flatten()[:total]
    flat_y = grid_y.flatten()[:total]

    step_y = (y_range[1] - y_range[0]) / rows
    flat_x += np.random.uniform(-step_x / coeficiente, step_x / coeficiente, total)
    flat_y += np.random.uniform(-step_y / coeficiente, step_y / coeficiente, total)

    zs = np.array([py5.random(*z_range) for _ in range(total)])

    return tuple(zip(flat_x, flat_y, zs, strict=True)), (step_x, step_y)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    meio_x = helpers.DIMENSOES.external[0] / 2
    meio_y = helpers.DIMENSOES.external[1] / 2
    x_range = -meio_x, meio_x + 1
    y_range = -meio_y, meio_y + 1
    z_range = -900, 40
    pontos, (passo_x, passo_y) = calcula_pontos(400, x_range, y_range, z_range)
    for x, y, z in pontos:
        paleta = paletas[0]
        passo = max([passo_x, passo_y])
        r_max = py5.random((passo), passo * 2)
        r_range = py5.random(r_max / 3.0, r_max / 1.8), r_max
        total = py5.random_int(5, 14)
        cor_1 = py5.random_choice(paleta)
        cor_2 = py5.random_choice(paleta)
        while cor_1 == cor_2:
            cor_2 = py5.random_choice(paleta)
        z_dist = float(py5.remap(z, z_range[0], z_range[1], 0, 1))
        CIRCULOS.append(calcula_circulos(x, y, z, z_dist, r_range, total, cor_1, cor_2))
        paletas.rotate()


def draw():
    py5.background("#010101")
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, -40)
        py5.no_fill()
        for figura in CIRCULOS:
            for info in figura.circulos:
                with py5.push():
                    py5.translate(0, 0, figura.z)
                    raio = info.raio
                    py5.stroke_weight(info.traco)
                    py5.stroke(info.cor)
                    py5.circle(figura.x, figura.y, raio)

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
