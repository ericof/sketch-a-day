from functools import cache

import numpy as np
import py5


def rgb_to_hsb(r: float, g: float, b: float) -> list[float]:
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

    hsb = [
        float(hue[0]),
        float(saturation[0]) * 100,
        float(brightness[0]) * 100,
    ]
    return hsb


def extrai_rgb(cor: int) -> tuple[float, float, float]:
    """Extrai os componentes R G B de uma cor."""
    return (py5.red(cor), py5.green(cor), py5.blue(cor))


def extrai_rgba(cor: int) -> tuple[float, float, float, float]:
    """Extrai os componentes R G B de uma cor."""
    return (py5.red(cor), py5.green(cor), py5.blue(cor), py5.alpha(cor))


@cache
def lerp_color_rgba(cor_1: int, cor_2: int, t) -> int:
    """Calcula uma cor intermediária entre duas cores."""
    r1, g1, b1, a1 = extrai_rgba(cor_1)
    r2, g2, b2, a2 = extrai_rgba(cor_2)
    t = py5.constrain(t, 0, 1)
    r = float(py5.lerp(r1, r2, t))
    g = float(py5.lerp(g1, g2, t))
    b = float(py5.lerp(b1, b2, t))
    a = float(py5.lerp(a1, a2, t))
    return py5.color(r, g, b, a)
