"""2025-07-31
Circularis strepitus VII
Grade de formas com uso de meia-esfera com pontos baseados em ruídos.
ericof.com|Inspirado em https://ericof.com/en/sketches/2023-05-25
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers

import numpy as np
import opensimplex
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

VERTICES = [
    (-150, -150, 60),
    (150, 150, 300),
    (-150, 150, 120),
    (150, -150, 180),
]


def meia_esfera(
    diametro: float,
    n: int,
    seed: int | None = None,
    distancia: float = 0.1,
    amplitude: float = 0.05,
    escala: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Gera uma meia esfera (z >= 0) e cria uma segunda versão com deslocamento radial.

    O deslocamento é sempre para fora do centro da esfera, e pode incluir ruído simplex.

    Args:
        diametro (float): Diâmetro da esfera.
        n (int): Número de pontos.
        seed (int | None): Semente para reprodutibilidade.
        distancia (float): Distância mínima radial a adicionar.
        amplitude (float): Intensidade do ruído adicionado à distancia.
        escala (float): Escala usada no ruído simplex.

    Returns:
        tuple[np.ndarray, np.ndarray]: pontos_originais e pontos_deslocados
    """
    if seed is not None:
        np.random.seed(seed)

    raio = diametro / 2

    # Coordenadas esféricas para meia esfera
    phi = np.random.uniform(0, 2 * np.pi, n)
    cos_theta = np.random.uniform(0, 1, n)
    theta = np.arccos(cos_theta)

    x = raio * np.sin(theta) * np.cos(phi)
    y = raio * np.sin(theta) * np.sin(phi)
    z = raio * np.cos(theta)

    pontos_originais = np.column_stack((x, y, z))

    # Vetores normalizados (unitários) do centro até cada ponto
    norm = np.linalg.norm(pontos_originais, axis=1, keepdims=True)
    unit_vectors = pontos_originais / norm

    # Distância radial: base + ruído
    distances = np.array([
        distancia
        + amplitude * opensimplex.noise3(xi * escala, yi * escala, zi * escala)
        for xi, yi, zi in pontos_originais
    ])

    pontos_deslocados = pontos_originais + unit_vectors * distances[:, np.newaxis]

    return pontos_originais, pontos_deslocados


def popula_pontos():
    interno, externo = meia_esfera(
        diametro=400, n=8000, seed=None, distancia=40, amplitude=20, escala=6
    )
    todos_pontos = []
    for v in VERTICES:
        pontos = []
        local = []
        for idx, ((xi, yi, zi), (xo, yo, zo)) in enumerate(
            zip(interno, externo, strict=True)
        ):
            local.append((xi, yi, zi, 0))
            local.append((xo, yo, zo, 1))
            if idx % 10 == 9:
                pontos.append(local)
                local = []
        if local:
            pontos.append(local)
        todos_pontos.append((v, pontos))
    return todos_pontos


def desenha_pontos(
    pontos,
    hb_range: tuple[float, float] = (0, 360),
):
    forma = py5.create_shape()
    cores = []
    externos = []
    with forma.begin_closed_shape():
        hb = py5.random_int(*hb_range)
        for x, y, z, externo in pontos:
            forma.vertex(x, y, z)
            if not externo:
                hb = py5.random_int(*hb_range)
            h = (360 - hb) if externo else hb
            s = 50 if externo else 100
            b = 100 * abs(z / 500) if externo else 100
            cor = py5.color(h, s, b)
            cores.append(cor)
            if externo:
                externos.append((x, y, z))
    forma.set_strokes(cores)
    forma.set_fill(False)
    py5.shape(forma)
    with py5.push():
        h = 360 - hb
        py5.stroke_weight(4)
        py5.stroke(h, 100, 50)
        for x, y, z in externos:
            py5.point(x, y, z)


TODOS_PONTOS = popula_pontos()


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color(0)
    py5.background(cor_fundo)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.frame_rate(5)


def draw():
    z = py5.frame_count * 10 - 100
    cor_fundo = py5.color(0)
    py5.background(cor_fundo)
    centro = (py5.width / 2, py5.height / 2)
    with py5.push():
        py5.translate(*centro, z)
        py5.rotate(py5.radians(45))
        for (x, y, hb), pontos_ in TODOS_PONTOS:
            with py5.push():
                py5.translate(x, y, 0)
                for pontos in pontos_:
                    desenha_pontos(pontos, hb_range=(hb, hb + 60))
    # Credits and go
    canvas.sketch_frame(
        sketch, cor_fundo, "large_transparent_white", "transparent_white"
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
