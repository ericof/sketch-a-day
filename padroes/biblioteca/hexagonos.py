import py5

from .. import tipos
from ._biblioteca import registra_padrao
from .utils import gera_forma


def gera_hexagono() -> py5.Py5Shape:
    forma = gera_forma(6)
    forma.rotate(py5.radians(30))
    return forma


@registra_padrao()
class HexagonoRaios(tipos.Padrao):
    categoria = "hexagonos"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        hexagono = gera_hexagono()
        hexagono.set_stroke_weight(self.traco)
        hexagono.set_stroke(cores.traco)
        hexagono.set_fill(False)
        passo = 0.75
        largura_max = self.largura * passo
        largura_min = 5
        largura = largura_max
        while largura > largura_min:
            y = -largura // 2
            pg.shape(hexagono, 0, y, largura, largura)
            largura *= passo
