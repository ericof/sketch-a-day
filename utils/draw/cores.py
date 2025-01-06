import numpy as np


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
