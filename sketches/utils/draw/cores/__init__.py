from functools import cache

import numpy as np
import py5


def rgb_hex_to_hsb(cor: str) -> tuple[float, float, float]:
    """Converte uma cor RGB hexadecimal em HSB.

    :param cor: Cor no formato hexadecimal ``rrggbb`` (com ou sem ``#`` inicial).
    :returns: Tupla ``(H, S, B)`` com matiz em [0, 360) e saturacao/brilho em
        [0, 100].
    :raises ValueError: Se a string nao tiver 6 digitos hexadecimais.
    """
    cor = cor[1:] if cor.startswith("#") else cor
    if len(cor) != 6:
        raise ValueError("A cor deve estar no formato RGB (6 caracteres).")
    r, g, b = int(cor[0:2], 16), int(cor[2:4], 16), int(cor[4:6], 16)
    return rgb_to_hsb(r, g, b)


def rgb_to_hsb(r: float, g: float, b: float) -> tuple[float, float, float]:
    """Converte componentes RGB em HSB.

    :param r: Componente vermelho em [0, 255].
    :param g: Componente verde em [0, 255].
    :param b: Componente azul em [0, 255].
    :returns: Tupla ``(H, S, B)`` com matiz em [0, 360), saturacao e brilho
        em [0, 100].
    """
    rgb = np.asarray(np.array([r, g, b]), dtype=float)
    if rgb.ndim == 1:
        rgb = rgb[np.newaxis, :]

    # Normalize RGB values to [0, 1]
    rgb = rgb / 255.0

    # Extract channels
    r, g, b = rgb[:, 0], rgb[:, 1], rgb[:, 2]

    # Compute Brightness
    brightness = np.max(rgb, axis=1)

    # Compute Saturation
    delta = np.max(rgb, axis=1) - np.min(rgb, axis=1)
    saturation = np.where(brightness == 0, 0, delta / brightness)

    # Compute Hue
    hue = np.zeros_like(brightness)
    mask = delta > 0

    # Red is the max
    hue[mask & (brightness == r)] = (60 * (g[mask] - b[mask]) / delta[mask]) % 360
    # Green is the max
    hue[mask & (brightness == g)] = (60 * (b[mask] - r[mask]) / delta[mask]) + 120
    # Blue is the max
    hue[mask & (brightness == b)] = (60 * (r[mask] - g[mask]) / delta[mask]) + 240

    hsb = (
        float(hue[0]),
        float(saturation[0]) * 100,
        float(brightness[0]) * 100,
    )
    return hsb


def extrai_rgb(cor: int) -> tuple[float, float, float]:
    """Extrai os componentes R G B de uma cor."""
    return (py5.red(cor), py5.green(cor), py5.blue(cor))


def extrai_rgba(cor: int) -> tuple[float, float, float, float]:
    """Extrai os componentes R, G, B e A de uma cor."""
    return (py5.red(cor), py5.green(cor), py5.blue(cor), py5.alpha(cor))


@cache
def lerp_color_rgba(
    cor_1: int, cor_2: int, t, t_min_max: tuple[int, int] = (0, 1)
) -> int:
    """Calcula uma cor intermediaria entre duas cores, interpolando RGBA.

    :param cor_1: Cor inicial, usada quando ``t`` esta no minimo.
    :param cor_2: Cor final, usada quando ``t`` esta no maximo.
    :param t: Fator de interpolacao, restringido a ``t_min_max``.
    :param t_min_max: Faixa ``(min, max)`` usada para limitar ``t``.
    :returns: Cor interpolada como inteiro py5.
    """
    r1, g1, b1, a1 = extrai_rgba(cor_1)
    r2, g2, b2, a2 = extrai_rgba(cor_2)
    t = py5.constrain(t, *t_min_max)
    r = float(py5.lerp(r1, r2, t))
    g = float(py5.lerp(g1, g2, t))
    b = float(py5.lerp(b1, b2, t))
    a = float(py5.lerp(a1, a2, t))
    return py5.color(r, g, b, a)
