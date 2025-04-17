from dataclasses import dataclass

import py5


@dataclass
class CoresPadrao:
    traco: py5.Py5Color
    preenchimento: py5.Py5Color
    fundo: py5.Py5Color


class Padrao:
    categoria: str
    centro: tuple[float, float]
    largura: float
    altura: float
    traco: float

    def __init__(self, largura: int = 100, altura: int = 100, traco: float = 1):
        self.largura = int(largura)
        self.altura = int(altura)
        self.centro = (largura / 2, altura / 2)
        self.traco = traco

    @property
    def nome(self) -> str:
        """Nome desse padrão."""
        return self.__class__.__name__

    def padrao(self, pg: py5.Py5Graphics, cores: CoresPadrao):
        pass

    def __call__(self, rotacao: float, cores: CoresPadrao) -> py5.Py5Graphics:
        pg = py5.create_graphics(self.largura, self.altura, py5.P3D)
        with pg.begin_draw():
            pg.stroke(self.traco)
            with pg.push_matrix():
                pg.translate(*self.centro)
                pg.rotate(py5.radians(rotacao))
                pg.background(cores.fundo)
                pg.stroke(cores.traco)
                pg.fill(cores.preenchimento)
                self.padrao(pg, cores)
        return pg


@dataclass
class Borda:
    cor: py5.Py5Color
    grossura: int = 0


class Celula:
    x: float
    y: float
    idx: int
    idy: int
    borda: Borda | None = None

    def __init__(
        self,
        x: float,
        y: float,
        largura: float,
        altura: float,
        idx: int,
        idy: int,
        borda: Borda | None = None,
    ):
        self.x = x
        self.idx = idx
        self.y = y
        self.idy = idy
        self.largura = largura
        self.altura = altura
        self.borda = borda

    def _desenha_borda(self):
        grossura = self.borda.grossura
        cor = self.borda.cor
        buffer = grossura / 2
        with py5.push():
            py5.rect_mode(py5.CORNER)
            py5.stroke(cor)
            py5.stroke_weight(grossura)
            py5.no_fill()
            py5.translate(self.x, self.y, -2)
            largura = self.largura + buffer * 2
            altura = self.largura + buffer * 2
            py5.rect(-buffer, -buffer, largura, altura)

    def __call__(
        self, padrao: Padrao, rotacao: float, cores: CoresPadrao
    ) -> py5.Py5Graphics:
        if self.borda:
            self._desenha_borda()
        with py5.push():
            py5.translate(self.x, self.y)
            imagem = padrao(rotacao, cores)
            py5.image(imagem, 0, 0, self.largura, self.altura)
