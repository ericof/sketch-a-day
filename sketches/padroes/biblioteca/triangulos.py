from .. import tipos
from ._biblioteca import registra_padrao

import py5


@registra_padrao()
class TrianguloCanto(tipos.Padrao):
    categoria = "triangulos"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        meio_x, meio_y = self.centro
        pg.triangle(-meio_x, -meio_y, -meio_x, meio_y, meio_x, meio_y)


@registra_padrao()
class TrianguloCantoDividido(tipos.Padrao):
    categoria = "triangulos"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke(self.traco)
        meio_x, meio_y = self.centro
        pg.triangle(-meio_x, -meio_y, -meio_x, meio_y, meio_x, meio_y)
        with py5.push():
            pg.fill(cores.traco)
            pg.triangle(0, 0, -meio_x, meio_y, meio_x, meio_y)


@registra_padrao()
class TrianguloMeio(tipos.Padrao):
    categoria = "triangulos"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        meio_x, meio_y = self.centro
        pg.triangle(0, 0, -meio_x, meio_y, meio_x, meio_y)


@registra_padrao()
class TrianguloMetades(tipos.Padrao):
    categoria = "triangulos"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        meio_x, meio_y = self.centro
        pg.triangle(0, 0, -meio_x, meio_y, meio_x, meio_y)
        pg.triangle(0, 0, -meio_x, -meio_y, meio_x, -meio_y)
