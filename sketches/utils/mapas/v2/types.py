from dataclasses import dataclass
from geopandas.geodataframe import GeoDataFrame
from typing import Any

import numpy as np


@dataclass
class PointFilter:
    coordinates: tuple[float, float]
    distance: float


@dataclass
class FeatureLayer:
    name: str
    tags: dict[str, Any]
    gdf: GeoDataFrame


@dataclass
class GeoDataV2:
    """Classe para armazenar dados geográficos obtidos do OSMnx."""

    name: str
    point: PointFilter
    boundary: tuple[np.float64, ...]
    features: dict[str, FeatureLayer]
    networks: dict[str, FeatureLayer]
