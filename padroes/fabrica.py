from collections.abc import Iterable, Iterator
from itertools import cycle
from random import choices

from . import tipos


def cria_celulas(
    largura, altura, colunas, linhas, espacamentos, borda: tipos.Borda | None = None
) -> list[tipos.Celula]:
    esp_x, esp_y = espacamentos
    celula_largura = (largura - (esp_x * (colunas - 1))) / colunas
    celula_altura = (altura - (esp_y * (linhas - 1))) / linhas
    celulas = []
    for idy in range(linhas):
        for idx in range(colunas):
            celula_x = (esp_x + celula_largura) * idx
            celula_y = (esp_y + celula_altura) * idy
            celula = tipos.Celula(
                celula_x, celula_y, celula_largura, celula_altura, idx, idy, borda
            )
            celulas.append(celula)
    return celulas


class GradeLinearPadroes:
    celulas: list[tipos.Celula]
    colecao: dict[str, tipos.Padrao]

    def __init__(
        self,
        largura: float,
        altura: float,
        colunas: int,
        linhas: int,
        espacamentos: tuple[float, float],
        colecao: Iterable[tipos.Padrao],
        padroes: Iterable[str] = (),
        borda: tipos.Borda | None = None,
    ):
        self.celulas = cria_celulas(
            largura, altura, colunas, linhas, espacamentos, borda
        )
        self.colecao = {p.nome: p for p in colecao}
        self._padroes = padroes

    @property
    def padroes(self) -> Iterator[tipos.Padrao]:
        padroes = self._padroes
        if not padroes:
            tamanho = len(self.celulas)
            padroes = choices([p for p in self.colecao], k=tamanho)
        lista_padroes = [self.colecao[p] for p in padroes]
        iterador = cycle(lista_padroes)
        return iterador
