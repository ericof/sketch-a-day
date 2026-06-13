"""Geracao de pontos sobre circunferencias para uso nos sketches.

Reune helpers que devolvem listas de pontos amostrados sobre um circulo,
tanto no plano XY (:func:`pontos_circulo`) quanto orientados livremente no
espaco 3D atraves de um vetor normal (:func:`pontos_circulo_3d`). As listas
retornadas sao pensadas para alimentar diretamente vertices de formas py5.
"""

import numpy as np
import py5


def pontos_circulo(
    total_pontos: int = 360, raio: float = 100.0, x0: float = 0.0, y0: float = 0.0
) -> list[tuple[float, float]]:
    """Gera pontos igualmente espacados sobre um circulo no plano XY.

    Amostra ``total_pontos`` ao longo de uma circunferencia de raio ``raio``
    centrada em ``(x0, y0)``, comecando no eixo x positivo (``angulo = 0``) e
    avancando em incrementos de ``360 / total_pontos`` graus.

    :param total_pontos: quantidade de pontos a amostrar sobre o circulo.
    :param raio: raio do circulo.
    :param x0: coordenada x do centro.
    :param y0: coordenada y do centro.
    :returns: lista de pares ``(x, y)`` na ordem de amostragem.
    """
    pontos = []

    for idx in range(total_pontos):
        angulo = 360 / total_pontos * idx
        x = x0 + (np.cos(py5.radians(angulo)) * raio)
        y = y0 + (np.sin(py5.radians(angulo)) * raio)
        pontos.append((x, y))
    return pontos


def pontos_circulo_3d(
    total_pontos: int = 360,
    raio: float = 100.0,
    x0: float = 0.0,
    y0: float = 0.0,
    z0: float = 0.0,
    normal: tuple[float, float, float] = (0, 0, 1),
) -> list[tuple[float, float, float]]:
    """Gera pontos sobre um circulo orientado livremente no espaco 3D.

    O circulo e construido no plano XY (com ``z = 0``) e em seguida rotacionado
    para que seu eixo aponte na direcao de ``normal``, sendo por fim transladado
    para o centro ``(x0, y0, z0)``. A rotacao alinha o eixo Z ``(0, 0, 1)`` --
    normal natural do plano XY -- ao vetor ``normal`` informado.

    A matriz de rotacao e montada pela formula de Rodrigues
    ``R = I + sin(theta) * K + (1 - cos(theta)) * K @ K``, onde ``K`` e a matriz
    antissimetrica do eixo de rotacao (produto vetorial entre Z e ``normal``) e
    ``theta`` e o angulo entre os dois vetores.

    :param total_pontos: quantidade de pontos a amostrar sobre o circulo.
    :param raio: raio do circulo.
    :param x0: coordenada x do centro.
    :param y0: coordenada y do centro.
    :param z0: coordenada z do centro.
    :param normal: vetor normal que define a orientacao do plano do circulo;
        nao precisa ser unitario, pois e normalizado internamente.
    :returns: lista de triplas ``(x, y, z)`` na ordem de amostragem.

    .. note::
        Quando ``normal`` e antiparalelo a Z (ex.: ``(0, 0, -1)``), o produto
        vetorial e nulo e a funcao usa a identidade como rotacao, sem aplicar o
        giro de 180 graus. Para a geometria do circulo isso e irrelevante (a
        forma e simetrica), mas a ordem/winding dos pontos fica como se a normal
        apontasse para ``+Z`` -- relevante apenas se o sentido da normal importar
        (iluminacao, face culling, normais manuais no P3D).
    """
    pontos = []

    # Normaliza o vetor normal (sem reatribuir o parametro tipado).
    normal_unit = np.asarray(normal, dtype=float)
    normal_unit = normal_unit / np.linalg.norm(normal_unit)

    # Eixo de rotacao: produto vetorial entre o eixo Z e a normal desejada.
    z_axis = np.array([0.0, 0.0, 1.0])
    rot_axis = np.cross(z_axis, normal_unit)
    rot_angle = np.arccos(np.clip(np.dot(z_axis, normal_unit), -1.0, 1.0))

    # Se ha rotacao a fazer, monta a matriz pela formula de Rodrigues.
    if np.linalg.norm(rot_axis) > 1e-6:
        rot_axis = rot_axis / np.linalg.norm(rot_axis)
        K = np.array([
            [0, -rot_axis[2], rot_axis[1]],
            [rot_axis[2], 0, -rot_axis[0]],
            [-rot_axis[1], rot_axis[0], 0],
        ])
        R = np.eye(3) + np.sin(rot_angle) * K + (1 - np.cos(rot_angle)) * np.dot(K, K)
    else:
        R = np.eye(3)  # Nenhuma rotacao necessaria (ja no plano XY).

    for idx in range(total_pontos):
        angulo = 360 / total_pontos * idx
        x = np.cos(py5.radians(angulo)) * raio
        y = np.sin(py5.radians(angulo)) * raio
        z = 0

        # Rotaciona o ponto em torno da origem.
        point = np.dot(R, np.array([x, y, z]))
        # Translada para o centro.
        point += np.array([x0, y0, z0])

        pontos.append(tuple(point))

    return pontos
