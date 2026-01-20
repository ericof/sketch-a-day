from pathlib import Path

import sketches


ROOT_FOLDER = Path(sketches.__file__).parent
RESOURCES_FOLDER = ROOT_FOLDER / "_resources"


def caminho_arquivo(filename: str) -> Path:
    """Retorna caminho de arquivo de recurso.

    Levanta exceção se arquivo não existir.
    """
    path = RESOURCES_FOLDER / filename
    if not path.exists():
        raise FileNotFoundError()
    return path


def carrega_aquivo_texto(filename: str) -> str:
    """Carrega arquivo texto e retorna seu conteúdo."""
    path = caminho_arquivo(filename)
    return path.read_text()
