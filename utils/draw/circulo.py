import numpy as np
import py5


def pontos_circulo(
    total_pontos: int = 360, raio: float = 100.0, x0: float = 0.0, y0: float = 0.0
):
    pontos = []

    for idx in range(total_pontos):
        angulo = 360 / total_pontos * idx
        x = x0 + (np.cos(py5.radians(angulo)) * raio)
        y = y0 + (np.sin(py5.radians(angulo)) * raio)
        pontos.append((x, y))
    return pontos
