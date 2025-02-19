from collections import deque
from dataclasses import dataclass

import py5


@dataclass
class Paleta:
    nome: str
    cores: list[str] | list[tuple[int, int, int]]
    tipo: int = py5.HSB
    ref: str = ""


PALETAS = {
    "laranja": Paleta(
        "laranja",
        [
            "#D24E01",
            "#DC6601",
            "#E27602",
            "#E88504",
            "#EC9005",
            "#EE9F27",
            "#F1B04C",
            "#F5C77E",
            "#F9DDB1",
        ],
        py5.RGB,
        "https://www.pinterest.com/pin/orange-color-palette--70437486736390/",
    ),
    "mondrian": Paleta(
        "mondrian",
        [
            "#F7D744",
            "#D0341E",
            "#D0341E",
            "#120D2D",
            "#425AC6",
            "#CAC9D1",
        ],
        py5.RGB,
        "https://www.colourlovers.com/palette/3991914/Mondrians_Crayons",
    ),
    "azul": Paleta(
        "azul",
        [
            "#0077B6",
            "#0096C7",
            "#00B4D8",
            "#023E8A",
            "#03045E",
            "#48CAE4",
            "#90E0EF",
            "#ADE8F4",
            "#CAF0F8",
        ],
        py5.RGB,
        "https://www.pinterest.com/pin/5136987069455448/",
    ),
}


def gera_paleta(
    nome: str, como_deque: bool = False
) -> list[py5.color] | deque[py5.color]:
    """Retorna lista de cores a partir da paleta escolhida."""
    if (paleta := PALETAS.get(nome)) is None:
        raise ValueError("Paleta desconhecida")
    resultado = []
    for cor in paleta.cores:
        if isinstance(cor, str):
            resultado.append(py5.color(cor))
        else:
            resultado.append(py5.color(*cor))
    return deque(resultado) if como_deque else resultado


__all__ = ["gera_paleta"]
