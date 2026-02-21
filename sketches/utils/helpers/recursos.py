from pathlib import Path

import py5
import sketches


PKG_FOLDER = Path(sketches.__file__).parent
RESOURCES_FOLDER = PKG_FOLDER / "_resources"
ROOT_FOLDER = PKG_FOLDER.parent
CACHE_FOLDER = ROOT_FOLDER / "cache"


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


def carrega_imagem_cache(filename: str) -> py5.Py5Image | None:
    """Carrega imagem do cache e retorna caminho do arquivo."""
    path = CACHE_FOLDER / filename
    if not path.exists():
        return None
    return py5.load_image(path)


def salva_imagem_cache(pg: py5.Py5Graphics, filename: str) -> Path:
    """Salva imagem em cache e retorna caminho do arquivo."""
    if not CACHE_FOLDER.exists():
        CACHE_FOLDER.mkdir()
    path = CACHE_FOLDER / filename
    img = pg.get_pixels()
    img.save(str(path))
    return path
