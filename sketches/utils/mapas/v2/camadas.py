from sketches.utils.mapas.v2 import types as t
from typing import Any

import osmnx as ox


def get_feature_layer(
    point: t.PointFilter, name: str, tags: dict[str, Any]
) -> t.FeatureLayer:
    """Obtém uma camada de features a partir de um ponto e tags."""
    feature_gdf = ox.features_from_point(
        point.coordinates, dist=point.distance, tags=tags
    )
    feature = t.FeatureLayer(name=name, tags=tags, gdf=feature_gdf)
    return feature
