import py5

from .. import tipos
from ._biblioteca import registra_padrao


class PadraoTraco(tipos.Padrao):
    categoria = "tracos"

    @property
    def retas(self) -> tuple[tuple[float, float, float, float], ...]:
        pass

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.no_fill()
        pg.stroke_weight(self.traco)
        for reta in self.retas:
            pg.line(*reta)


@registra_padrao()
class TracoCentralMetade(PadraoTraco):
    @property
    def retas(self) -> tuple[tuple[float, float, float, float], ...]:
        largura = self.largura // 2
        x0, y0 = 0, 0
        x1 = x0
        y1 = y0 + largura
        return ((x0, y0, x1, y1),)


@registra_padrao()
class TracoCentralCompleto(PadraoTraco):
    @property
    def retas(self) -> tuple[tuple[float, float, float, float], ...]:
        largura = self.largura // 2
        x0, y0 = 0, -largura
        x1 = x0
        y1 = largura
        return ((x0, y0, x1, y1),)


@registra_padrao()
class TracosCantos(PadraoTraco):
    @property
    def retas(self) -> tuple[tuple[float, float, float, float], ...]:
        largura = self.largura // 2
        return (
            (-largura, -largura, largura, largura),
            (0, -largura, 0, largura),
            (-largura, largura, largura, -largura),
        )


@registra_padrao()
class TracosCruzados(PadraoTraco):
    @property
    def retas(self) -> tuple[tuple[float, float, float, float], ...]:
        largura = self.largura // 2
        return (
            (-largura, -largura, largura, largura),
            (-largura, largura, largura, -largura),
        )


@registra_padrao()
class TracosSeta(PadraoTraco):
    @property
    def retas(self) -> tuple[tuple[float, float, float, float], ...]:
        largura = self.largura // 2
        return (
            (-largura, -largura, 0, 0),
            (-largura, largura, 0, 0),
        )


@registra_padrao()
class TracosReto(PadraoTraco):
    @property
    def retas(self) -> tuple[tuple[float, float, float, float], ...]:
        largura = self.largura // 2
        return (
            (0, 0, 0, largura),
            (0, 0, largura, 0),
        )


@registra_padrao()
class TracoCirculoCentralP(PadraoTraco):
    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.no_fill()
        pg.stroke_weight(self.traco)
        pg.circle(0, 0, self.largura * 0.25)


@registra_padrao()
class TracoCirculoCentral(PadraoTraco):
    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.no_fill()
        pg.stroke_weight(self.traco)
        pg.circle(0, 0, self.largura // 2)


@registra_padrao()
class TracoCirculoCentralG(PadraoTraco):
    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.no_fill()
        pg.stroke_weight(self.traco)
        pg.circle(0, 0, self.largura * 0.75)
