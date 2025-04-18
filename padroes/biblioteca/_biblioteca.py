from collections import defaultdict

from .. import tipos as t

__all__ = ["Biblioteca", "registra_padrao"]


class BibliotecaClass:
    padroes: dict[str, t.Padrao]
    categorias: dict[str, dict[str, t.Padrao]]

    def __init__(self):
        self.categorias = defaultdict(dict)
        self.padroes = {}

    def get_categoria(self, categoria: str) -> dict[str, t.Padrao]:
        return self.categorias[categoria]

    def get_padrao(self, nome: str) -> t.Padrao:
        return self.padroes[nome]


Biblioteca = BibliotecaClass()


class registra_padrao:
    """Registra um padrão em nossa biblioteca."""

    def __init__(self):
        pass

    def __call__(self, padrao: t.Padrao):
        categoria = padrao.categoria
        nome = padrao.__name__
        Biblioteca.categorias[categoria][nome] = padrao
        Biblioteca.padroes[nome] = padrao
        return padrao
