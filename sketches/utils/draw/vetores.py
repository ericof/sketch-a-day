import numpy as np


def criar_vetor(x: float, y: float) -> np.ndarray:
    """Cria um vetor 2D (NumPy) como array float64 de shape (2,)."""
    return np.array([x, y], dtype=np.float64)


def interpolar_vetor(v1: np.ndarray, v2: np.ndarray, t: float) -> np.ndarray:
    """Interpola linearmente entre v1 e v2 com fator t em [0, 1]."""
    return v1 + (v2 - v1) * t


def calcular_cruzamento(
    a1: np.ndarray, a2: np.ndarray, b1: np.ndarray, b2: np.ndarray
) -> np.ndarray:
    """Interseção das retas a1-a2 e b1-b2 (linhas infinitas)."""
    a1x, a1y = a1
    a2x, a2y = a2
    b1x, b1y = b1
    b2x, b2y = b2

    aa1 = a1y - a2y
    bb1 = a2x - a1x
    cc1 = a1x * a2y - a2x * a1y

    aa2 = b1y - b2y
    bb2 = b2x - b1x
    cc2 = b1x * b2y - b2x * b1y

    denominador = aa1 * bb2 - aa2 * bb1
    x = (bb1 * cc2 - bb2 * cc1) / denominador
    y = (aa2 * cc1 - aa1 * cc2) / denominador
    return criar_vetor(float(x), float(y))


def normal_90(v: np.ndarray) -> np.ndarray:
    """Rotaciona v 90° (x,y)->(-y,x) sem trigonometria."""
    x, y = v
    return criar_vetor(-y, x)


def ajustar_magnitude(v: np.ndarray, mag: float) -> np.ndarray:
    """Retorna v com magnitude mag (evita chamadas caras de API)."""
    vx, vy = v
    norma = float(np.hypot(vx, vy))
    if norma == 0.0:
        return criar_vetor(0.0, 0.0)
    escala = mag / norma
    return criar_vetor(vx * escala, vy * escala)
