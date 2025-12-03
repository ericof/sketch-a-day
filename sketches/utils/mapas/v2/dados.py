from pathlib import Path
from sketches.utils.mapas.v2 import types as t

import osmnx.settings as ox_settings
import pickle


DATA_FILENAME = "osmnx.data"


def inicializa_osmnx(log_console: bool = False, requests_timeout: int = 1000) -> None:
    """Inicializa configurações do OSMnx."""
    ox_settings.log_console = log_console
    ox_settings.requests_timeout = requests_timeout


def carrega_osmnx_dados(pasta: Path) -> t.GeoDataV2 | None:
    """Carrega dados do OSMnx a partir de um arquivo pickle na pasta especificada."""
    data_path = pasta / DATA_FILENAME
    if data_path.is_file():
        with open(data_path, "rb") as f:
            geodata = pickle.load(f)  # noQA: S301
        return geodata


def salva_osmnx_dados(pasta: Path, geodata: t.GeoDataV2) -> None:
    """Salva dados do OSMnx em um arquivo pickle na pasta especificada."""
    data_path = pasta / DATA_FILENAME
    with open(data_path, "wb") as f:
        pickle.dump(geodata, f)
