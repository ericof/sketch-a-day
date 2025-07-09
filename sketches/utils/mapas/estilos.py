from dataclasses import dataclass

import py5


@dataclass
class EstiloElemento:
    """Estilos para um elemento."""

    exibir: bool = True
    stroke: int | None = py5.color("#FFF")
    stroke_weight: float = 1.0
    fill: int | None = None


__ESTILOS__ = {
    "simples": {
        "default": (True, "#FFF", 1.0, "#FFF"),
        "clinic": (True, "#FFF", 1.0, "#FFF"),
        "grassland": (True, "#7CFC00", 1.0, "#7CFC00"),
        "library": (True, "#000", 1.0, "#CCC"),
        "place_of_worship": (True, "#000", 1.0, "#000"),
        "sand": (True, "#C2B280", 0.5, "#C2B280"),
        "water": (True, "#0000FF", 2.0, "#0000FF"),
        "wood": (True, "#9D6C3C", 1.0, "#9D6C3C"),
    }
}


def get_paleta_estilos(nome: str) -> dict[str, EstiloElemento]:
    """Retorna a paleta de estilos para o nome especificado.

    Args:
        nome (str): Nome da paleta de estilos.

    Returns:
        dict[str, EstiloElemento]: Dicionário com os estilos.
    """
    if nome in __ESTILOS__:
        paleta = {}
        for k, raw_value in __ESTILOS__[nome].items():
            value = []
            for idx, v in enumerate(raw_value):
                if idx in (1, 3) and v is not None:
                    v = py5.color(v)
                value.append(v)
            paleta[k] = EstiloElemento(*value)
    return paleta
