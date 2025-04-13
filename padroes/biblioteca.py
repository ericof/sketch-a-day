import py5

from . import tipos


class CirculoCanto(tipos.Padrao):
    nome = "CirculoCanto"
    categoria = "circulo"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        pg.ellipse_mode(py5.CENTER)
        pg.circle(*self.centro, self.largura * 2)


class CirculoCentroP(tipos.Padrao):
    nome = "CirculoCentroP"
    categoria = "circulo"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        pg.ellipse_mode(py5.CENTER)
        pg.circle(0, 0, self.largura // 3)


class CirculoCentroM(tipos.Padrao):
    nome = "CirculoCentroM"
    categoria = "circulo"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        pg.ellipse_mode(py5.CENTER)
        pg.circle(0, 0, self.largura // 2)


class CirculoConncentrico(tipos.Padrao):
    nome = "CirculoConncentrico"
    categoria = "circulo"

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
    nome = "Raios"
    categoria = "circulo"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        pg.ellipse_mode(py5.CENTER)
        with py5.push():
            py5.no_stroke()
            for raio in range(self.largura * 2, 5, -10):
                pg.circle(*self.centro, raio)
