from dataclasses import dataclass

import py5


@dataclass
class EstiloCaminho:
    """Estilos para um caminho."""

    exibir: bool = True
    stroke: int | None = py5.color("#888888")
    stroke_weight: float = 0.0
    fill: int | None = py5.color("#888888")


@dataclass
class EstiloElemento:
    """Estilos para um elemento."""

    exibir: bool = True
    stroke: int | None = py5.color("#FFF")
    stroke_weight: float = 1.0
    fill: int | None = None


__ESTILOS__ = {
    "simples": {
        "caminhos": {
            "default": (True, "#888888", 3.0, None),
            "footway": (True, "#CCCCCC", 3.0, None),
            "pedestrian": (True, "#CCCCCC", 3.0, None),
            "steps": (True, "#888888", 3.0, None),
            "residential": (True, "#888888", 3.0, None),
        },
        "elementos": {
            "default": (True, "#FFFFFF", 1.0, "#FFFFFF"),
            "building": (True, "#FFFFFF", 1.0, "#FFFFFF"),
            "clinic": (True, "#FFFFFF", 1.0, "#FFFFFF"),
            "grassland": (True, "#7CFC00", 0.0, "#7CFC00"),
            "library": (True, "#000000", 1.0, "#CCCCCC"),
            "park": (True, "#056D05", 0.0, "#056D05"),
            "parking": (True, "#AAAAAA", 0.0, "#AAAAAA"),
            "pitch": (True, "#7CFC00", 0.0, "#7CFC00"),
            "place_of_worship": (True, "#000", 1.0, "#000"),
            "sand": (True, "#C2B280", 0.5, "#C2B280"),
            "school": (True, "#000000", 1.0, "#CCCCCC"),
            "water": (True, "#0000FF", 2.0, "#0000FF"),
            "wood": (True, "#9D6C3C", 1.0, "#9D6C3C"),
        },
    }
}


def get_paleta_estilos(
    nome: str, categoria: str = "elementos"
) -> dict[str, EstiloElemento | EstiloCaminho]:
    """Retorna a paleta de estilos para o nome especificado.

    Args:
        nome (str): Nome da paleta de estilos.
        categoria (str): Elemento ou caminho para o qual os estilos são aplicados.

    Returns:
        dict[str, EstiloElemento]: Dicionário com os estilos.
    """
    if nome in __ESTILOS__:
        if categoria == "caminhos":
            klass = EstiloCaminho
            data = __ESTILOS__[nome]["caminhos"]
        else:
            klass = EstiloElemento
            data = __ESTILOS__[nome]["elementos"]
        paleta = {}
        for k, raw_value in data.items():
            value = []
            for idx, v in enumerate(raw_value):
                if idx in (1, 3) and v is not None:
                    v = py5.color(v)
                value.append(v)
            paleta[k] = klass(*value)
    return paleta
