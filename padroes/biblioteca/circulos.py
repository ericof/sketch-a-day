import py5

from .. import tipos
from ._biblioteca import registra_padrao


@registra_padrao()
class CirculoCanto(tipos.Padrao):
    categoria = "circulos"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        pg.ellipse_mode(py5.CENTER)
        pg.circle(*self.centro, self.largura * 2)


@registra_padrao()
class CirculoCentroP(tipos.Padrao):
    categoria = "circulos"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        pg.ellipse_mode(py5.CENTER)
        pg.circle(0, 0, self.largura // 3)


@registra_padrao()
class CirculoCentroM(tipos.Padrao):
    categoria = "circulos"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        pg.ellipse_mode(py5.CENTER)
        pg.circle(0, 0, self.largura // 2)


@registra_padrao()
class CirculoConncentrico(tipos.Padrao):
    categoria = "circulos"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        pg.ellipse_mode(py5.CENTER)
        with py5.push():
            pg.fill(cores.traco)
            pg.stroke(cores.preenchimento)
            pg.circle(0, 0, self.largura // 2)
        with py5.push():
            pg.stroke(cores.traco)
            pg.fill(cores.preenchimento)
            pg.circle(0, 0, self.largura // 3)


@registra_padrao()
class RaiosCanto(tipos.Padrao):
    categoria = "circulos"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        pg.ellipse_mode(py5.CENTER)
        with py5.push():
            pg.no_fill()
            for raio in range(self.largura * 2, 5, -10):
                pg.circle(*self.centro, raio)


@registra_padrao()
class CirculosRaios(tipos.Padrao):
    categoria = "circulos"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        pg.ellipse_mode(py5.CENTER)
        passo = 0.75
        largura_max = self.largura * passo
        largura_min = 5
        largura = largura_max
        with py5.push():
            pg.no_fill()
            while largura > largura_min:
                pg.circle(0, 0, largura)
                largura *= passo
