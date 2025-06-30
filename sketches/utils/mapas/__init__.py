from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from geopandas.geodataframe import GeoDataFrame
from networkx import MultiDiGraph
from pathlib import Path
from shapely.affinity import affine_transform

import numpy as np
import osmnx as ox
import pickle
import py5
import shapely


data_filename = "osmnx.data"


@dataclass
class Camada:
    """Classe para armazenar uma camada de dados geográficos."""

    nome: str
    gdf: GeoDataFrame


@dataclass
class Geodata:
    """Classe para armazenar dados geográficos obtidos do OSMnx."""

    bbox: tuple[float, float, float, float]
    graph: MultiDiGraph
    camadas: list[Camada]


@dataclass
class GeodataEscalado:
    """Dados escalados."""

    _raw: Geodata
    bbox: tuple[float, float, float, float]
    camadas: list[Camada]


def _expandir_bbox(
    bbox: np.ndarray | tuple[float, float, float, float], percentual: float = 10.0
) -> tuple[float, float, float, float]:
    """
    Expande uma bounding box geográfica EPSG:4326, recebida como np.array,
    de forma que o resultado seja sempre 10% maior em largura e altura.

    Parâmetros:
    - bbox: np.array([long_min, lat_min, long_max, lat_max])
    - percentual: porcentagem de expansão (padrão: 10%)

    Retorna:
    - nova tuple([long_min, lat_min, long_max, lat_max]) expandida
    """
    long_min, lat_min, long_max, lat_max = bbox

    largura = long_max - long_min
    altura = lat_max - lat_min

    margem_long = largura * (percentual / 100) / 2
    margem_lat = altura * (percentual / 100) / 2

    return (
        long_min - margem_long,
        lat_min - margem_lat,
        long_max + margem_long,
        lat_max + margem_lat,
    )


def obtem_dados(regiao: str, pasta: Path, tags: tuple[str] = ("building",)) -> Geodata:
    """Obtém dados geográficos para uma região específica."""
    if (data_path := pasta / data_filename).is_file():
        with open(data_path, "rb") as f:
            geodata = pickle.load(f)  # noQA: S301
    else:
        payload = dict.fromkeys(tags, True)
        limites = ox.geocode_to_gdf(regiao)
        bbox_limites = _expandir_bbox(limites.total_bounds, percentual=20)
        graph = ox.graph_from_bbox(bbox_limites)
        gdf_nodes, gdf_edges = ox.graph_to_gdfs(
            graph, nodes=True, edges=True, node_geometry=True, fill_edge_geometry=False
        )
        elementos = ox.features_from_bbox(bbox=bbox_limites, tags=payload)
        geodata = Geodata(
            bbox=bbox_limites,
            graph=graph,
            camadas=[
                Camada(nome="pontos", gdf=gdf_nodes),
                Camada(nome="caminhos", gdf=gdf_edges),
                Camada(nome="elementos", gdf=elementos),
                Camada(nome="limites", gdf=limites),
            ],
        )
        with open(data_path, "wb") as f:
            pickle.dump(geodata, f)
    return geodata


def remapear_geodataframe_com_bbox(
    gdf: GeoDataFrame,
    bbox_origem: tuple[float, float, float, float],
    bbox_destino: tuple[float, float, float, float],
) -> GeoDataFrame:
    """
    Reprojeta as geometrias de um GeoDataFrame: limites de origem -> limites de destino.

    Ambos os limites devem estar no formato:
    (long_min, lat_min, long_max, lat_max)

    A função calcula a transformação afim necessária para encaixar as geometrias
    do sistema de coordenadas original no novo sistema de referência
    (ex: canvas de visualização).

    Parâmetros:
    - gdf: GeoDataFrame com geometria em EPSG:4326
    - bbox_origem: limites originais (long_min, lat_min, long_max, lat_max)
    - bbox_destino: limites alvo (x_min, y_min, x_max, y_max) — ex: (0, 800, 800, 0)
                    para tela invertida

    Retorna:
    - GeoDataFrame com geometrias transformadas para o novo espaço
    """
    long_min_o, lat_min_o, long_max_o, lat_max_o = bbox_origem
    x_min_d, y_min_d, x_max_d, y_max_d = bbox_destino

    # Verifica se o bbox original é válido
    if long_min_o == long_max_o or lat_min_o == lat_max_o:
        raise ValueError("Limites de origem inválidos: largura ou altura igual a zero.")

    # Cálculo das escalas com detecção de inversão
    escala_x = (x_max_d - x_min_d) / (long_max_o - long_min_o)
    escala_y = (y_max_d - y_min_d) / (lat_max_o - lat_min_o)

    def transformar_geometria(geometria):
        if geometria is None or geometria.is_empty:
            return geometria
        return affine_transform(
            geometria,
            [
                escala_x,
                0,
                0,
                escala_y,
                -long_min_o * escala_x + x_min_d,
                -lat_min_o * escala_y + y_min_d,
            ],
        )

    gdf_transformado = gdf.copy()
    gdf_transformado["geometry"] = gdf_transformado["geometry"].apply(
        transformar_geometria
    )
    return gdf_transformado


def escala_dados(
    dados: Geodata,
    coordenadas: tuple[float, float, float, float] = (0, 800, 800, 0),
) -> GeodataEscalado:
    """Escala os dados geográficos para a largura e altura especificadas."""
    camadas = []
    limites_origem = dados.bbox
    for camada in dados.camadas:
        if not isinstance(camada.gdf, GeoDataFrame):
            continue
        gdf = remapear_geodataframe_com_bbox(camada.gdf, limites_origem, coordenadas)
        camadas.append(Camada(nome=camada.nome, gdf=gdf))
    return GeodataEscalado(
        _raw=dados,
        bbox=coordenadas,
        camadas=camadas,
    )


def processa_elementos(
    paleta: deque[py5.Py5Color],
    area_min: float = 5.0,
    stroke: py5.Py5Color | None = None,
    stroke_weight: int = 0,
) -> Callable:
    """Processa a camada de elementos para desenhar o mapa."""

    def func(gdf: GeoDataFrame) -> list[py5.Py5Shape]:
        camadas = []
        for g, _ in zip(gdf.geometry, gdf.amenity, strict=True):
            # Ignora geometrias sem indicação de uso
            if g.area < area_min:
                continue
            cor = py5.color(paleta[0])
            paleta.rotate()
            elemento = py5.convert_shape(g)
            if stroke is not None:
                elemento.set_stroke(stroke)
                elemento.set_stroke_weight(stroke_weight)
            else:
                elemento.set_stroke_weight(0)
            elemento.set_fill(cor)
            camadas.append(elemento)
        return camadas

    return func


def processa_caminhos(stroke: py5.Py5Color, stroke_weight: int = 1) -> Callable:
    """Processa a camada de caminhos para desenhar as rotas de um mapa."""

    def func(gdf: GeoDataFrame) -> list[py5.Py5Shape]:
        caminhos = dataframe_para_shape(gdf)
        caminhos.set_stroke(py5.color(255))
        return [
            caminhos,
        ]

    return func


def mapa_como_forma(
    dados: GeodataEscalado, cor_fundo: py5.Py5Color, camadas: list[tuple[str, Callable]]
) -> py5.Py5Shape:
    largura, altura = (
        abs(dados.bbox[2] - dados.bbox[0]),
        abs(dados.bbox[3] - dados.bbox[1]),
    )
    forma = py5.create_shape(py5.GROUP)
    # Cria o fundo do mapa
    fundo = py5.create_shape(py5.RECT, 0, 0, largura, altura)
    fundo.set_fill(cor_fundo)
    fundo.set_stroke(py5.color(0))
    fundo.set_stroke_weight(2)
    forma.add_child(fundo)
    todas_camadas = {c.nome: c.gdf for c in dados.camadas}
    # Camadas
    for nome, func in camadas:
        gdf = todas_camadas.get(nome)
        if gdf is None or gdf.empty:
            continue
        for camada in func(gdf):
            forma.add_child(camada)
    return forma


def dataframe_para_shape(gdf: GeoDataFrame) -> py5.Py5Shape:
    shps = shapely.GeometryCollection(tuple(gdf.geometry))
    return py5.convert_shape(shps)
