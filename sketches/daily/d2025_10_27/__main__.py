"""2025-10-27
Circularis strepitus redux 06
Criação de uma meia-esfera com pontos baseados em ruído.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import numpy as np
import opensimplex
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)


def meia_esfera(
    diametro: float,
    n: int,
    seed: int | None = None,
    distancia: float = 0.1,
    amplitude: float = 0.15,
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
        diametro=120, n=12000, seed=None, distancia=180, amplitude=60, escala=12
    )
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
    return pontos


def desenha_pontos(pontos, paleta):
    forma = py5.create_shape()
    cores = []
    externos = []
    cor_principal = paleta[0]
    with forma.begin_closed_shape():
        for x, y, z, externo in pontos:
            if externo:
                externos.append((x, y, z))
                continue
            cor = paleta[0]
            cores.append(cor)
            forma.vertex(x, y, z)
            paleta.rotate(1)
    forma.set_strokes(cores)
    forma.set_fill(False)
    py5.shape(forma)
    with py5.push():
        py5.stroke_weight(4)
        py5.stroke(cor_principal)
        for idx, (x, y, z) in enumerate(externos):
            paleta.rotate(1)
            if idx % 15 != 0:
                continue
            elif idx % 45 == 0:
                py5.stroke_weight(8)
            else:
                py5.stroke_weight(4)
            py5.stroke(paleta[0])
            py5.point(x, y, z)


PONTOS = popula_pontos()


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color(0)
    py5.background(cor_fundo)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.frame_rate(5)


def draw():
    paleta = gera_paleta("laranja-01", True)
    z = py5.frame_count * 5 - 100
    cor_fundo = py5.color(0)
    py5.background(cor_fundo)
    centro = (py5.width / 2, py5.height / 2)
    with py5.push():
        py5.translate(*centro, z)
        for pontos in PONTOS:
            desenha_pontos(pontos, paleta=paleta)
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
