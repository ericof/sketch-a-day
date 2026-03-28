from .. import tipos as t
from collections import defaultdict


__all__ = ["Biblioteca", "registra_padrao"]


class BibliotecaClass:
    padroes: dict[str, type[t.Padrao]]
    categorias: dict[str, dict[str, type[t.Padrao]]]

    def __init__(self):
        self.categorias = defaultdict(dict)
        self.padroes = {}

    def get_categoria(self, categoria: str) -> dict[str, type[t.Padrao]]:
        return self.categorias[categoria]

    def get_padrao(self, nome: str) -> type[t.Padrao]:
        return self.padroes[nome]

    def get_padroes(self) -> dict[str, type[t.Padrao]]:
        return self.padroes


Biblioteca = BibliotecaClass()


class registra_padrao:
    """Registra um padrão em nossa biblioteca."""

    def __init__(self):
        pass

    def __call__(self, padrao: type[t.Padrao]):
        categoria = padrao.categoria
        nome = padrao.__name__
        Biblioteca.categorias[categoria][nome] = padrao
        Biblioteca.padroes[nome] = padrao
        return padrao
