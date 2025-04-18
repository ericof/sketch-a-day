import py5

from .. import tipos
from ._biblioteca import registra_padrao


@registra_padrao()
class QuadradoCentro(tipos.Padrao):
    categoria = "quadrados"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        pg.rect_mode(py5.CENTER)
        largura = self.largura // 2
        pg.rect(0, 0, largura, largura)


@registra_padrao()
class QuadradoCanto(tipos.Padrao):
    categoria = "quadrados"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        pg.rect_mode(py5.CORNER)
        largura = self.largura // 2
        pg.rect(-largura, -largura, largura, largura)


@registra_padrao()
class QuadradoCantos(tipos.Padrao):
    categoria = "quadrados"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        pg.rect_mode(py5.CORNER)
        largura = self.largura // 2
        pg.rect(-largura, -largura, largura, largura)
        pg.rect(largura, largura, -largura, -largura)


@registra_padrao()
class QuadradoMetade(tipos.Padrao):
    categoria = "quadrados"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        pg.rect_mode(py5.CORNER)
        largura = self.largura // 2
        pg.rect(-largura, -largura, largura, self.largura)
