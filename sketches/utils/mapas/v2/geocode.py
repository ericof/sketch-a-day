from sketches.utils.mapas.v2 import types as t

import numpy as np
import osmnx as ox


def geocode_boundary(
    address: str,
) -> tuple[np.float64, ...]:
    """Obtém os limites geocodificados a partir de um endereço."""
    return tuple(ox.geocode_to_gdf(address).total_bounds)


def geocode_point(address: str, distance: float) -> t.PointFilter:
    """Obtém um ponto geocodificado a partir de um endereço."""
    point = ox.geocode(address)
    return t.PointFilter(coordinates=point, distance=distance)
