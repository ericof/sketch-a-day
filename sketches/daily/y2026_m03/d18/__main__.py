"""2026-03-18
Manchas concêntricas 01
Distribuição de círculos concêntricos
ericof.com
png
Sketch,py5,CreativeCoding
"""

from dataclasses import dataclass
from sketches.utils.draw import canvas
from sketches.utils.draw.cores import lerp_color_rgba
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
paleta: list[int] = gera_paleta("mondrian")


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
    traco_base = dist_media / 2
    t_minmax = (0, num)
    for idx in range(num):
        cor = lerp_color_rgba(cor_1, cor_2, idx, t_minmax)
        raios.append(
            CirculoRaio(
                raio=(dist_media + py5.random_int(-3, 3)) * idx + inicial,
                cor=cor,
                traco=traco_base * py5.random(0.2, 0.75),
            )
        )
    return raios


def calcula_circulos(
    x_range: tuple[float, float],
    y_range: tuple[float, float],
    z_range: tuple[float, float],
    r_range: tuple[float, float],
    total: int,
    cor_1: int,
    cor_2: int,
) -> CirculosConcentricos:
    x = py5.random(*x_range)
    y = py5.random(*y_range)
    z = py5.random(*z_range)
    circulos = calcula_raios(total, cor_1, cor_2, *r_range)
    return CirculosConcentricos(x=x, y=y, z=z, circulos=circulos)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    meio_x = helpers.DIMENSOES.external[0] / 2
    meio_y = helpers.DIMENSOES.external[1] / 2
    x_range = -meio_x, meio_x + 1
    y_range = -meio_y, meio_y + 1
    z_range = -400, 20
    for _ in range(300):
        r_min = py5.random_int(20, 50)
        r_range = r_min, py5.random_int(int(r_min * 1.5), int(r_min * 3))
        total = py5.random_int(5, 11)
        cor_1 = py5.random_choice(paleta)
        cor_2 = py5.random_choice(paleta)
        while cor_1 == cor_2:
            cor_2 = py5.random_choice(paleta)
        CIRCULOS.append(
            calcula_circulos(x_range, y_range, z_range, r_range, total, cor_1, cor_2)
        )


def draw():
    py5.background("#444444")
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
