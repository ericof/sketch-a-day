from pathlib import Path
from sketches.utils.mapas.v2 import camadas as c_utils
from sketches.utils.mapas.v2 import dados as d_utils
from sketches.utils.mapas.v2 import geocode as g_utils
from sketches.utils.mapas.v2 import types as t
from typing import Any


def _obtem_dados_osmnx(
    pasta: Path,
    limite: str,
    endereco: str,
    distancia: float,
    camadas: dict[str, dict[str, Any]],
    caminhos: dict[str, dict[str, Any]],
) -> t.GeoDataV2:
    """Obtém dados do OSMnx a partir de um arquivo pickle na pasta especificada."""
    boundary = g_utils.geocode_boundary(limite)
    gpoint = g_utils.geocode_point(address=endereco, distance=distancia)
    geodata = t.GeoDataV2(endereco, gpoint, boundary=boundary, features={}, networks={})
    for name, camada in camadas.items():
        layer = c_utils.get_feature_layer(
            point=gpoint,
            name=name,
            tags=camada["tag"],
        )
        geodata.features[name] = layer
    for name, caminho in caminhos.items():
        layer = c_utils.get_feature_layer(
            point=gpoint,
            name=name,
            tags=caminho["tag"],
        )
        geodata.networks[name] = layer
    d_utils.salva_osmnx_dados(pasta, geodata)
    return geodata


def obtem_dados_osmnx(
    pasta: Path,
    limite: str,
    endereco: str,
    distancia: float,
    camadas: dict[str, dict[str, Any]],
    caminhos: dict[str, dict[str, Any]],
) -> t.GeoDataV2:
    """Obtém dados do OSMnx a partir de um arquivo pickle na pasta especificada."""
    geodata = d_utils.carrega_osmnx_dados(pasta)
    if not geodata:
        geodata = _obtem_dados_osmnx(
            pasta=pasta,
            limite=limite,
            endereco=endereco,
            distancia=distancia,
            camadas=camadas,
            caminhos=caminhos,
        )
    return geodata


def translate_and_scale_gdf(gdf, x, y, x_scale, y_scale):
    gdf["geometry"] = gdf.geometry.translate(x, y)
    gdf["geometry"] = gdf.geometry.scale(xfact=x_scale, yfact=y_scale, origin=(0, 0))
