from .recursos import carrega_aquivo_texto


def resource_text(filename: str) -> str:
    """Open a text file from the resource folder."""
    return carrega_aquivo_texto(filename)
