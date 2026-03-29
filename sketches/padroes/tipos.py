from dataclasses import dataclass

import py5


@dataclass
class CoresPadrao:
    """Conjunto de cores usado para renderizar um padrão."""

    traco: int
    preenchimento: int
    fundo: int | None = None


class Padrao:
    """Classe base para padrões vetoriais renderizados em um buffer gráfico.

    Subclasses devem implementar :meth:`padrao` para definir o desenho.
    O padrão é sempre desenhado com origem no centro do buffer.
    """

    categoria: str
    centro: tuple[float, float]
    largura: float
    altura: float
    traco: float

    def __init__(self, largura: float = 100, altura: float = 100, traco: float = 1):
        """Inicializa o padrão com as dimensões e espessura de traço.

        :param largura: Largura do buffer em pixels.
        :param altura: Altura do buffer em pixels.
        :param traco: Espessura base do traço.
        """
        self.largura = float(largura)
        self.altura = float(altura)
        self.centro = (self.largura / 2, self.altura / 2)
        self.traco = traco

    @property
    def nome(self) -> str:
        """Nome desse padrão."""
        return self.__class__.__name__

    def padrao(self, pg: py5.Py5Graphics, cores: CoresPadrao) -> None:
        """Desenha o padrão no buffer gráfico.

        :param pg: Buffer gráfico com origem já transladada para o centro.
        :param cores: Cores a usar no desenho.
        """
        pass

    def __call__(self, rotacao: float, cores: CoresPadrao) -> py5.Py5Graphics:
        """Renderiza o padrão e retorna o buffer gráfico resultante.

        :param rotacao: Ângulo de rotação em graus.
        :param cores: Cores a usar no desenho.
        :returns: Buffer :class:`py5.Py5Graphics` com o padrão renderizado.
        """
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
    """Borda decorativa ao redor de uma célula."""

    cor: int
    grossura: int = 0


class Celula:
    """Célula de uma grade que posiciona e renderiza um padrão no sketch.

    Armazena a posição ``(x0, y0)`` do canto superior esquerdo e ``(x, y)``
    do centro, além das dimensões da célula.
    """

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
        """Inicializa a célula.

        :param x: Coordenada x do canto superior esquerdo.
        :param y: Coordenada y do canto superior esquerdo.
        :param largura: Largura da célula em pixels.
        :param altura: Altura da célula em pixels.
        :param idx: Índice da coluna na grade.
        :param idy: Índice da linha na grade.
        :param borda: Borda opcional ao redor da célula.
        """
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
        """Desenha a borda ao redor da célula, se definida."""
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
        """Renderiza o padrão e, opcionalmente, o desenha na posição da célula.

        :param padrao: Padrão a renderizar.
        :param rotacao: Ângulo de rotação em graus.
        :param cores: Cores a usar no desenho.
        :param desenha: Se ``False``, retorna ``None`` sem desenhar.
        :param z: Coordenada z opcional para translação 3D.
        :returns: A imagem renderizada, ou ``None`` se *desenha* for ``False``.
        """
        if not desenha:
            return None
        pg = padrao(rotacao, cores)
        pg.load_pixels()
        imagem = py5.create_image(pg.pixel_width, pg.pixel_height, py5.ARGB)
        imagem.load_pixels()
        imagem.pixels[:] = pg.pixels[:]
        imagem.update_pixels()
        coordenadas: list[float] = [self.x, self.y]
        if self.borda:
            self._desenha_borda()
        if z is not None:
            coordenadas.append(z)
        with py5.push():
            py5.translate(*coordenadas)
            py5.image_mode(py5.CENTER)
            py5.image(imagem, 0, 0, int(self.largura), int(self.altura))
        return imagem
