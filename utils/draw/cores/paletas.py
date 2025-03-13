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
    "mandarin-redux": Paleta(
        "mandarin-redux",
        [
            "#F6724B",
            "#F87A4E",
            "#FA8251",
            "#FC8A55",
            "#D77653",
            "#B36252",
            "#8F4E51",
            "#6D454E",
            "#4C3C4B",
            "#2B3349",
            "#283651",
            "#25395A",
            "#223C63",
        ],
        py5.RGB,
        "Extrrapolation of mandarin",
    ),
    "sunset-ocean": Paleta(
        "sunset-ocean",
        [
            "#F89999",
            "#DC8F9D",
            "#C086A1",
            "#A57DA5",
            "#8973A9",
            "#6E6AAD",
            "#5261B1",
            "#3757B5",
            "#1B4EB9",
            "#0045BE",
        ],
        py5.RGB,
        "Gradient from #F89999 to #0045BE",
    ),
    "DJ1": Paleta(
        "DJ1",
        [
            "#A1C8D9",
            "#21617D",
            "#000405",
            "#2A784C",
            "#52C491",
            "#A1C8D9",
            "#21617D",
            "#000405",
        ],
        py5.RGB,
        "https://www.colourlovers.com/palette/4962911/DJ_1",
    ),
    "Navy-Orange": Paleta(
        "Navy-Orange",
        [
            "#FFB300",
            "#FFD700",
            "#00B2D0",
            "#00879E",
            "#003092",
            "#FFB300",
            "#FFD700",
            "#00B2D0",
        ],
        py5.RGB,
        "https://www.colourlovers.com/palette/4962954/navy_orange",
    ),
    "Colerful": Paleta(
        "Colerful",
        [
            "#7EC0E0",
            "#1C8EAF",
            "#032035",
            "#FDAA08",
            "#F87109",
        ],
        py5.RGB,
        "Reuso de paleta de sketches antigos",
    ),
}


def lista_paletas() -> list[str]:
    """Retorna lista de nomes de paletas."""
    paletas = sorted(list(PALETAS.keys()))
    return paletas


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


__all__ = ["gera_paleta", "lista_paletas"]
