from pathlib import Path
from PIL import Image

import numpy as np
import py5
import sketches
import tempfile


ROOT_FOLDER = Path(sketches.__file__).parent
RESOURCES_FOLDER = ROOT_FOLDER / "_resources"

__all__ = [
    "image_as_array",
    "resource_image_as_array",
    "save_frame",
]


def image_as_array(path: Path) -> np.ndarray:
    """Abre um arquivo de imagem e retorna como array NumPy.

    :param path: Caminho do arquivo de imagem.
    :returns: Array NumPy com os dados da imagem.
    """
    image = Image.open(path)
    return np.array(image)


def resource_image_as_array(filename: str) -> np.ndarray:
    """Abre uma imagem da pasta de recursos e retorna como array NumPy.

    :param filename: Nome do arquivo na pasta de recursos.
    :returns: Array NumPy com os dados da imagem.
    """
    path = RESOURCES_FOLDER / filename
    return image_as_array(path)


def tmp_path() -> Path:
    """Cria e retorna o caminho de um diretório temporário.

    :returns: Caminho do diretório temporário criado.
    """
    return Path(tempfile.mkdtemp())


def save_frame(tmp_path: Path, img_name: str, frame: int) -> Path:
    """Salva o frame atual do py5 como imagem PNG.

    :param tmp_path: Diretório temporário para salvar o frame.
    :param img_name: Nome base do arquivo de imagem.
    :param frame: Número do frame.
    :returns: Caminho do arquivo PNG salvo.
    """
    path = tmp_path / f"{img_name}_{frame:03d}.png"
    py5.save_frame(path)
    return path
