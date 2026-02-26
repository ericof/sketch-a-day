import numpy as np


def vizinhos_knn_esfera(pontos: np.ndarray, idx: int, k: int = 6) -> np.ndarray:
    """Calcula vizinhos para um ponto.

    pontos: (N, 3)
    idx: índice do ponto base
    k: número de vizinhos desejado
    retorna: índices dos k vizinhos mais próximos (por distância angular)
    """
    if pontos.ndim != 2 or pontos.shape[1] != 3:
        raise ValueError("pontos precisa ter shape (N, 3)")
    n = pontos.shape[0]
    if not (0 <= idx < n):
        raise IndexError("idx fora do range")
    if k <= 0:
        return np.array([], dtype=int)
    if n <= 1:
        return np.array([], dtype=int)

    # normaliza para raio 1 (remove efeito do raio na métrica angular)
    p = pontos / np.linalg.norm(pontos, axis=1, keepdims=True)

    # similaridade angular = cos(angulo) = dot(u, v); maior => mais perto
    sims = p @ p[idx]
    sims[idx] = -np.inf  # exclui o próprio ponto

    k = min(k, n - 1)
    # pega top-k por similaridade (sem ordenar tudo)
    nn = np.argpartition(-sims, kth=k - 1)[:k]
    # opcional: ordenar do mais próximo para o menos próximo
    nn = nn[np.argsort(-sims[nn])]
    return nn


def pontos_esfera(
    raio: float,
    num_pontos: int = 50,
) -> tuple[tuple[float, float, float], ...]:
    """
    Gera pontos em uma esfera centrada em (0, 0, 0).

    :param raio: Raio da esfera
    :param num_pontos: Número de subdivisões para theta e phi
    :return: Tupla de tuplas (x, y, z)
    """
    if num_pontos <= 0:
        return ()

    indices = np.arange(num_pontos)

    # Golden angle in radians
    golden_angle = np.pi * (3.0 - np.sqrt(5.0))

    y = 1.0 - (2.0 * indices) / (num_pontos - 1)  # y goes from 1 to -1
    radius_xy = np.sqrt(1.0 - y * y)

    theta = golden_angle * indices

    x = np.cos(theta) * radius_xy
    z = np.sin(theta) * radius_xy

    points = np.stack((x, y, z), axis=-1) * raio

    return tuple(map(tuple, points))
