from .. import tipos
from ._biblioteca import registra_padrao

import py5


class PadraoOndas(tipos.Padrao):
    categoria = "ondas"

    @property
    def pontos(self) -> tuple[tuple[float, float], ...]:
        return ()

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.no_fill()
        pg.stroke_weight(self.traco)
        for linha in self.pontos:
            x0, y0 = None, None
            for x, y in linha:
                if x0 is None:
                    x0, y0 = x, y
                pg.line(x0, y0, x, y)
                x0, y0 = x, y


class OndasParalelas(PadraoOndas):
    ciclos: int = 4
    min_max: tuple[int, int] = (0, 1)

    @property
    def pontos(self) -> tuple[tuple[float, float], ...]:
        x_min = int(-self.largura * 3)
        x_max = int(x_min * -1)
        passo = (x_max - x_min) / (360 / self.ciclos)
        distancia = (self.largura / 3) - (self.largura / 2)
        pontos = []
        for idy in range(*self.min_max):
            linha = []
            yb = distancia * idy
            for idx, x in enumerate(range(x_min, x_max)):
                y = int((py5.sin(py5.radians(idx * passo)) * distancia) + yb)
                linha.append((x, y))
            pontos.append(tuple(linha))
        return tuple(pontos)


@registra_padrao()
class OndasParalelas3(OndasParalelas):
    min_max: tuple[int, int] = (-1, 2)


@registra_padrao()
class OndasParalelas5(OndasParalelas):
    min_max: tuple[int, int] = (-2, 3)
