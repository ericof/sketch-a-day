from dataclasses import dataclass

import py5


@dataclass
class CoresPadrao:
    traco: int
    preenchimento: int
    fundo: int | None = None


class Padrao:
    categoria: str
    centro: tuple[float, float]
    extremidades: tuple[
        tuple[float, float],
        tuple[float, float],
        tuple[float, float],
        tuple[float, float],
    ]
    largura: float
    altura: float
    traco: float

    def __init__(self, largura: float = 100, altura: float = 100, traco: float = 1):
        self.largura = int(largura)
        self.altura = int(altura)
        metade_largura = largura / 2
        metade_altura = altura / 2
        self.centro = (metade_largura, metade_altura)
        self.traco = traco

    @property
    def nome(self) -> str:
        """Nome desse padrão."""
        return self.__class__.__name__

    def padrao(self, pg: py5.Py5Graphics, cores: CoresPadrao) -> None:
        pass

    def __call__(self, rotacao: float, cores: CoresPadrao) -> py5.Py5Graphics:
        pg = py5.create_graphics(int(self.largura), int(self.altura), py5.P3D)
        with pg.begin_draw():
            pg.stroke(self.traco)
            with pg.push():
                pg.translate(*self.centro)
                pg.rotate(py5.radians(rotacao))
                if cores.fundo:
                    pg.background(cores.fundo)
                pg.stroke(cores.traco)
                pg.fill(cores.preenchimento)
                self.padrao(pg, cores)
        return pg


@dataclass
class Borda:
    cor: int
    grossura: int = 0


class Celula:
    x: float
    y: float
    x0: float
    y0: float
    largura: float
    altura: float
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
        self.idx = idx
        self.idy = idy
        self.x0 = x
        self.y0 = y
        self.x = x + largura / 2
        self.y = y + altura / 2
        self.largura = largura
        self.altura = altura
        self.borda = borda

    def _desenha_borda(self) -> None:
        if not self.borda:
            return
        grossura = self.borda.grossura
        cor = self.borda.cor
        buffer = grossura / 2
        with py5.push():
            py5.rect_mode(py5.CORNER)
            py5.stroke(cor)
            py5.stroke_weight(grossura)
            py5.no_fill()
            py5.translate(self.x0, self.y0, -2)
            largura = self.largura + buffer * 2
            altura = self.altura + buffer * 2
            py5.rect(-buffer, -buffer, largura, altura)

    def __call__(
        self,
        padrao: Padrao,
        rotacao: float,
        cores: CoresPadrao,
        desenha: bool = True,
        z: float | None = None,
    ) -> py5.Py5Image | None:
        if not desenha:
            return
        pg = padrao(rotacao, cores)
        pg.load_pixels()
        pixels = pg.pixels[:]
        imagem = py5.create_image(pg.width, pg.height, py5.ARGB)
        imagem.load_pixels()
        for i in range(len(pixels)):
            imagem.pixels[i] = pixels[i]
        imagem.update_pixels()
        coordenadas = [self.x, self.y]
        if self.borda:
            self._desenha_borda()
        if z is not None:
            coordenadas.append(z)
        with py5.push():
            py5.translate(*coordenadas)
            py5.image_mode(py5.CENTER)
            py5.image(imagem, 0, 0)
        return imagem
