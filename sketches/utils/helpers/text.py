from .recursos import carrega_aquivo_texto


def resource_text(filename: str) -> str:
    """Carrega e retorna o conteúdo de um arquivo texto da pasta de recursos.

    :param filename: Nome do arquivo na pasta de recursos.
    :returns: Conteúdo do arquivo texto.
    """
    return carrega_aquivo_texto(filename)
