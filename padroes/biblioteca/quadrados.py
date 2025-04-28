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


@registra_padrao()
class QuadradoTotal(tipos.Padrao):
    categoria = "quadrados"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        largura = self.largura // 2
        pg.rect_mode(py5.CORNER)
        with py5.push():
            pg.stroke_weight(self.traco)
            pg.rect(-largura, -largura, self.largura, self.largura)


@registra_padrao()
class QuadradoVazio(tipos.Padrao):
    categoria = "quadrados"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pass


@registra_padrao()
class QuadradoRaios(tipos.Padrao):
    categoria = "quadrados"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        pg.rect_mode(py5.CENTER)
        passo = 0.75
        largura_max = self.largura * passo
        largura_min = 5
        largura = largura_max
        with py5.push():
            pg.no_fill()
            while largura > largura_min:
                pg.rect(0, 0, largura, largura)
                largura *= passo
