import py5

from . import tipos


class CirculoCanto(tipos.Padrao):
    categoria = "circulos"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        pg.ellipse_mode(py5.CENTER)
        pg.circle(*self.centro, self.largura * 2)


class CirculoCentroP(tipos.Padrao):
    categoria = "circulos"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        pg.ellipse_mode(py5.CENTER)
        pg.circle(0, 0, self.largura // 3)


class CirculoCentroM(tipos.Padrao):
    categoria = "circulos"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        pg.ellipse_mode(py5.CENTER)
        pg.circle(0, 0, self.largura // 2)


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


class TrianguloCanto(tipos.Padrao):
    categoria = "triangulos"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        meio_x, meio_y = self.centro
        pg.triangle(-meio_x, -meio_y, -meio_x, meio_y, meio_x, meio_y)


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


class TrianguloMeio(tipos.Padrao):
    categoria = "triangulos"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        meio_x, meio_y = self.centro
        pg.triangle(0, 0, -meio_x, meio_y, meio_x, meio_y)


class TrianguloMetades(tipos.Padrao):
    categoria = "triangulos"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        meio_x, meio_y = self.centro
        pg.triangle(0, 0, -meio_x, meio_y, meio_x, meio_y)
        pg.triangle(0, 0, -meio_x, -meio_y, meio_x, -meio_y)
