import py5

from .. import tipos
from ._biblioteca import registra_padrao


@registra_padrao()
class AzulejoQuadradoRaios(tipos.Padrao):
    categoria = "bulcao"

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        pg.stroke_weight(self.traco)
        # Quadrado
        centro_x, centro_y = self.centro
        with pg.push():
            pg.rect_mode(py5.CENTER)
            pg.fill(cores.traco)
            largura_quadrado = self.largura * 0.25
            pg.square(centro_x, centro_y, largura_quadrado)
        # Raios
        with pg.push():
            pg.no_fill()
            traco_max = self.traco * 5
            traco_min = self.traco * 2
            largura_max = self.largura * 2
            largura_min = largura_max - largura_quadrado
            arcos = [
                (largura_max - traco_max, traco_max),
                (largura_min + traco_min, traco_min),
            ]
            for largura, traco in arcos:
                pg.stroke_weight(traco)
                pg.arc(
                    centro_x,
                    centro_y,
                    largura,
                    largura,
                    py5.radians(180),
                    py5.radians(270),
                )


class AzulejoTresTracosBase(tipos.Padrao):
    categoria = "bulcao_tres_tracos"
    raios: int = 3
    traco_mult: int = 5
    espaco_mult: int = 3
    grupos: tuple[tuple[float, str], ...] = ((2, "traco"),)
    ang_inicio: float = py5.radians(180)
    ang_fim: float = py5.radians(270)

    def desenha_raios(
        self,
        pg: py5.Py5Graphics,
        centro: tuple[float, float],
        largura_max: float,
        altura_max: float,
        cor: py5.Py5Color,
    ):
        traco = self.traco * self.traco_mult
        espaco = self.traco * self.espaco_mult
        centro_x, centro_y = centro
        pg.stroke_weight(traco)
        pg.stroke(cor)
        with pg.push():
            pg.no_fill()
            largura = largura_max - traco
            altura = altura_max - traco
            for _ in range(self.raios):
                pg.arc(
                    centro_x,
                    centro_y,
                    largura,
                    altura,
                    self.ang_inicio,
                    self.ang_fim,
                )
                largura -= (traco * 2) + espaco
                altura -= (traco * 2) + espaco

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        for distancia, nome_cor in self.grupos:
            cor = getattr(cores, nome_cor)
            largura = self.largura * distancia
            self.desenha_raios(pg, self.centro, largura, largura, cor)


@registra_padrao()
class AzulejoTresTracos1(AzulejoTresTracosBase):
    grupos: tuple[float, ...] = ((2, "traco"),)


@registra_padrao()
class AzulejoTresTracos2(AzulejoTresTracosBase):
    grupos: tuple[float, ...] = ((2, "traco"), (1.2, "preenchimento"))


@registra_padrao()
class AzulejoTresTracos3(AzulejoTresTracosBase):
    ang_inicio: float = py5.radians(185)
    ang_fim: float = py5.radians(270)

    def desenha_retas(
        self, pg: py5.Py5Graphics, traco: float, espaco: float
    ) -> list[tuple[float, float, float, float]]:
        y0 = self.largura / 2
        pg.stroke_weight(traco)
        retas = []
        for idx in range(-1, 2):
            y1 = -traco
            x = idx * (traco + espaco)
            retas.append((x, y0, x, y1))

        with pg.push():
            for reta in retas:
                pg.line(*reta)
        return retas

    def padrao(self, pg: py5.Py5Graphics, cores: tipos.CoresPadrao) -> None:
        """Implementa padrão."""
        traco = self.traco * self.traco_mult
        espaco = self.traco * self.espaco_mult * 0.5
        # Retas
        retas = self.desenha_retas(pg, traco, espaco)
        # Arcos
        centro = self.centro[0], 0
        largura = self.largura - (retas[0][0] - traco - 4 * espaco) + 1
        altura = self.largura
        self.desenha_raios(pg, centro, largura, altura, cores.traco)
