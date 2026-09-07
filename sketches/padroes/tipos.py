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
    densidade: int

    def __init__(
        self,
        largura: float = 100,
        altura: float = 100,
        traco: float = 1,
        densidade: int = 1,
    ):
        """Inicializa o padrão com as dimensões e espessura de traço.

        :param largura: Largura nominal do padrão em pixels.
        :param altura: Altura nominal do padrão em pixels.
        :param traco: Espessura base do traço.
        :param densidade: Fator de supersampling do buffer. Com ``2``, o padrão
            é rasterizado no dobro da resolução e a imagem devolvida tem o dobro
            do lado; compor essa imagem no tamanho nominal rende bordas mais
            suaves. Só vale a pena quando o destino é menor que a imagem — ver
            :meth:`__call__`.
        """
        self.largura = float(largura)
        self.altura = float(altura)
        self.centro = (self.largura / 2, self.altura / 2)
        self.traco = traco
        self.densidade = int(densidade)

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

    def __call__(self, rotacao: float, cores: CoresPadrao) -> py5.Py5Image:
        """Renderiza o padrão e retorna a imagem resultante.

        O desenho acontece num :class:`py5.Py5Graphics`, mas o retorno é uma
        :class:`py5.Py5Image` com os pixels copiados, e isso não é detalhe de
        implementação: num display Retina o buffer reporta ``pixel_density``
        igual a 2 enquanto rasteriza em 1x, de modo que :func:`py5.image` pede
        uma região-fonte do dobro do tamanho da textura. As coordenadas passam
        de ``1.0``, clampam na borda, e o resultado é o quadrante superior-
        esquerdo do padrão ampliado com faixas esticadas no resto. Uma
        ``Py5Image`` não carrega densidade e compõe corretamente.

        A imagem devolvida tem lado ``largura * densidade``. Com *densidade*
        maior que ``1``, componha-a explicitamente no tamanho nominal — a forma
        de três argumentos de :func:`py5.image` usa o tamanho nativo e
        desenharia o padrão grande demais.

        :param rotacao: Ângulo de rotação em graus.
        :param cores: Cores a usar no desenho.
        :returns: Imagem :class:`py5.Py5Image` com o padrão renderizado.
        """
        densidade = self.densidade
        pg = py5.create_graphics(
            int(self.largura * densidade), int(self.altura * densidade), py5.P3D
        )
        with pg.begin_draw():
            pg.scale(densidade)
            pg.stroke(self.traco)
            with pg.push():
                pg.translate(*self.centro)
                pg.rotate(py5.radians(rotacao))
                if cores.fundo:
                    pg.background(cores.fundo)
                pg.stroke(cores.traco)
                pg.fill(cores.preenchimento)
                self.padrao(pg, cores)
        pg.load_pixels()
        imagem = py5.create_image(pg.pixel_width, pg.pixel_height, py5.ARGB)
        imagem.load_pixels()
        imagem.pixels[:] = pg.pixels[:]
        imagem.update_pixels()
        return imagem


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

    def _desenha_borda(self, pg: py5.Py5Graphics | None = None) -> None:
        """Desenha a borda ao redor da célula, se definida."""
        if not self.borda:
            return
        grossura = self.borda.grossura
        cor = self.borda.cor
        buffer = grossura / 2
        canvas = pg if pg is not None else py5
        with canvas.push():
            canvas.rect_mode(py5.CORNER)
            canvas.stroke(cor)
            canvas.stroke_weight(grossura)
            canvas.no_fill()
            canvas.translate(self.x0, self.y0, -2)
            largura = self.largura + buffer * 2
            altura = self.altura + buffer * 2
            canvas.rect(-buffer, -buffer, largura, altura)

    def __call__(
        self,
        padrao: Padrao,
        rotacao: float,
        cores: CoresPadrao,
        desenha: bool = True,
        z: float | None = None,
        pg: py5.Py5Graphics | None = None,
    ) -> py5.Py5Image | None:
        """Renderiza o padrão e, opcionalmente, o desenha na posição da célula.

        :param padrao: Padrão a renderizar.
        :param rotacao: Ângulo de rotação em graus.
        :param cores: Cores a usar no desenho.
        :param desenha: Se ``False``, retorna ``None`` sem desenhar.
        :param z: Coordenada z opcional para translação 3D.
        :param pg: Buffer alvo do desenho; ``None`` desenha no canvas principal.
        :returns: A imagem renderizada, ou ``None`` se *desenha* for ``False``.
        """
        if not desenha:
            return None
        imagem = padrao(rotacao, cores)
        coordenadas: list[float] = [self.x, self.y]
        if self.borda:
            self._desenha_borda(pg)
        if z is not None:
            coordenadas.append(z)
        canvas = pg if pg is not None else py5
        with canvas.push():
            canvas.translate(*coordenadas)
            canvas.image_mode(py5.CENTER)
            canvas.image(imagem, 0, 0, int(self.largura), int(self.altura))
        return imagem
