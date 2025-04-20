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
    "Warhol": Paleta(
        "Warhol",
        [
            "#FF007F",  # Hot Pink (Background)
            "#007FFF",  # Electric Blue (Foreground)
            "#FFFF33",  # Bright Yellow (Background)
            "#00FFFF",  # Cyan (Foreground)
            "#40E0D0",  # Turquoise (Background)
            "#FF1744",  # Deep Red (Foreground)
            "#FF6F00",  # Vivid Orange (Background)
            "#008080",  # Teal (Foreground)
            "#32CD32",  # Lime Green (Background)
            "#FF00FF",  # Magenta (Foreground)
            "#800080",  # Deep Purple (Background)
            "#FFFF00",  # Neon Yellow (Foreground)
            "#FF0000",  # Bright Red (Background)
            "#87CEEB",  # Sky Blue (Foreground)
            "#39FF14",  # Neon Green (Background)
            "#FF69B4",  # Hot Pink (Foreground)
        ],
        py5.RGB,
        "Andy Warhol's Marilyn Monroe",
    ),
    "oliver-13": Paleta(
        "oliver-13",
        [
            "#FFFFFF",  # White
            "#FFFBEA",  # Soft Cream
            "#FFF6D5",  # Light Ivory
            "#FFF0BF",  # Warm Ivory
            "#FFEAA9",  # Pale Gold
            "#FFE493",  # Light Goldenrod
            "#FFDE7D",  # Golden Haze
            "#FFD866",  # Dandelion
            "#FFD250",  # Golden Yellow
            "#FFCC3A",  # Amber Glow
            "#FFC624",  # Amber
            "#FFB800",  # Honey Gold
            "#FF9600",  # Deep Gold
            "#FF7A00",  # Rich Gold
        ],
        py5.RGB,
        "Paleta de 13 tons de amarelo",
    ),
    "maria-12": Paleta(
        "maria-12",
        [
            "#FFFFFF",  # White
            "#EAF3FF",  # Very Pale Blue
            "#D4E7FF",  # Pale Sky Blue
            "#BFDBFF",  # Light Baby Blue
            "#A9CFFF",  # Soft Ice Blue
            "#94C3FF",  # Powder Blue
            "#7EB7FF",  # Sky Blue
            "#69AAFF",  # Light Azure
            "#539EFF",  # Dodger Blue
            "#3E92FF",  # Bright Cornflower
            "#2886FF",  # Vivid Blue
            "#137AFF",  # Royal Blue
            "#006EFF",  # Strong Blue
        ],
        py5.RGB,
        "Paleta de 13 tons de amarelo",
    ),
    "brasil-01": Paleta(
        "brasil-01",
        [
            "#009739",  # Green (Ordem e Progresso background)
            "#FFCC29",  # Yellow (diamond shape)
            "#002776",  # Blue (globe with stars)
            "#FFFFFF",  # White (stars and band)
        ],
        py5.RGB,
        "Paleta com as cores da bandeira do Brasil",
    ),
    "brasil-02": Paleta(
        "brasil-02",
        [
            "#FFCC29",  # Yellow (diamond shape)
            "#002776",  # Blue (globe with stars)
        ],
        py5.RGB,
        "Paleta com as cores da bandeira do Brasil",
    ),
    "franca-01": Paleta(
        "franca-01",
        [
            "#0055A4",  # Blue (left stripe)
            "#FFFFFF",  # White (middle stripe)
            "#EF4135",  # Red (right stripe)
        ],
        py5.RGB,
        "Paleta com as cores da bandeira da França",
    ),
    "italia-01": Paleta(
        "italia-01",
        [
            "#009246",  # Green (left stripe)
            "#FFFFFF",  # White (middle stripe)
            "#CE2B37",  # Red (right stripe)
        ],
        py5.RGB,
        "Paleta com as cores da bandeira da Itália",
    ),
    "basco-01": Paleta(
        "basco-01",
        [
            "#D52B1E",  # Red (background of the flag)
            "#007A33",  # Green (St. Andrew's cross)
            "#FFFFFF",  # White (cross)
        ],
        py5.RGB,
        "Paleta com as cores da bandeira do País Basco",
    ),
}


def lista_paletas() -> list[str]:
    """Retorna lista de nomes de paletas."""
    paletas = sorted(list(PALETAS.keys()))
    return paletas


def gera_paleta(
    nome: str, como_deque: bool = False
) -> list[py5.Py5Color] | deque[py5.Py5Color]:
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
