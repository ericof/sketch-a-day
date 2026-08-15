"""2026-08-15
Particles 03
Sistema de partículas dinâmico com divisão e movimento giratório.
ericof.com|https://ericof.com/en/sketches/2025-12-15
png
Sketch,py5,CreativeCoding
"""

from matplotlib.colors import ListedColormap
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.grade import cria_grade_ex
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color("#000000")


particulas = []

PASSO: int = 120
DIAMETRO: float = 24.0
DDX: float = 0.990
REPETICOES: int = 10
Z_BASE: int = -50
PASSO_Z: int = 10
PALETA: str = "bright-colors"


def cmap_da_paleta(nome: str) -> ListedColormap:
    """Converte uma paleta do pacote numa colormap do matplotlib.

    Ponto de extensão: :func:`gera_paleta` devolve uma lista discreta de cores,
    enquanto o modo ``CMAP`` do py5 espera uma colormap indexável por um valor
    numérico. Aqui cada cor da paleta vira um degrau da colormap, sem
    interpolação entre elas — o índice cai num degrau e a cor sai exatamente
    como está na paleta.

    Cada cor é um :class:`py5.Py5Color`, que é um inteiro ARGB; os componentes
    saem por deslocamento de bits porque :func:`py5.red` e companhia exigem um
    sketch em execução e esta função roda em escopo de módulo.

    :param nome: nome de uma paleta conhecida por :func:`gera_paleta`.
    :returns: colormap aceita por :func:`py5.color_mode` em modo ``CMAP``.
    :raises ValueError: se a paleta não existir no pacote.
    """
    cores = [int(cor) for cor in gera_paleta(nome)]
    return ListedColormap(
        [
            (((cor >> 16) & 0xFF) / 255, ((cor >> 8) & 0xFF) / 255, (cor & 0xFF) / 255)
            for cor in cores
        ],
        name=nome,
    )


cmap_paleta = cmap_da_paleta(PALETA)


class Particula:
    """Partícula circular que se desloca em arco, encolhe, se divide e morre.

    Cada partícula vive num plano ``z`` fixo e percorre o canvas com a
    velocidade girando sempre para o mesmo lado (:attr:`sentido`), o que traça
    arcos em vez de retas. A cada quadro o diâmetro é multiplicado por
    :data:`DDX`, então ela encolhe continuamente; abaixo de 1 pixel se remove da
    lista global ``particulas``. Enquanto vive, tem uma pequena chance por
    quadro de gerar uma cópia de si mesma no mesmo ponto, com a velocidade
    invertida — é essa divisão que povoa o sketch.
    """

    def __init__(
        self,
        x,
        y,
        z,
        diametro=None,
        velocidade=None,
        sentido=None,
        paleta: ListedColormap | None = None,
    ):
        """Cria uma partícula em ``(x, y)`` sobre o plano ``z``.

        :param x: coordenada horizontal inicial, em pixels.
        :param y: coordenada vertical inicial, em pixels.
        :param z: profundidade do plano em que a partícula é desenhada.
        :param diametro: diâmetro inicial em pixels; sorteado entre 20 e 50
            quando omitido.
        :param velocidade: deslocamento por quadro como :class:`py5.Py5Vector2D`;
            sorteado em direção aleatória com módulo 2 quando omitido.
        :param sentido: ``-1`` ou ``1``, o lado para o qual a velocidade gira;
            sorteado quando omitido.
        :param paleta: colormap consultada em :meth:`desenha`, construída a
            partir de uma paleta do pacote por :func:`cmap_da_paleta`.
        """
        self.pos = py5.Py5Vector(x, y)
        self.z = z
        self.velocidade = velocidade or py5.Py5Vector2D.random() * 2
        self.diametro = diametro or py5.random(20, 50)
        self.sentido = sentido or py5.random_choice((-1, 1))
        self.paleta = paleta

    def atualiza(self):
        """Avança a partícula um quadro: desenha, move, encolhe, divide, morre.

        A ordem importa — a partícula é desenhada na posição em que estava antes
        do movimento deste quadro. Em seguida o diâmetro é multiplicado por
        :data:`DDX`; há cerca de 2% de chance de gerar uma filha na posição
        atual, com a velocidade invertida e o mesmo sentido de giro e paleta; e,
        se o diâmetro cair abaixo de 1 pixel, a partícula se remove da lista
        global ``particulas``.
        """
        self.desenha()
        self.movimenta()
        self.diametro = self.diametro * DDX
        if py5.random(100) < 2:
            particulas.append(
                Particula(
                    self.pos.x,
                    self.pos.y,
                    self.z,
                    self.diametro,
                    -self.velocidade,
                    sentido=self.sentido,
                    paleta=self.paleta,
                )
            )
        if self.diametro < 1:
            particulas.remove(self)

    def desenha(self):
        """Desenha a partícula como um círculo preenchido, sem contorno.

        A cor sai da paleta da própria partícula: o diâmetro atual é remapeado
        de ``0..DIAMETRO`` para ``0..255`` e usado como índice na colormap, de
        modo que encolher é também percorrer a paleta. A opacidade recebe um
        ruído pequeno a cada quadro, o que dá textura ao acúmulo.
        """
        with py5.push():
            py5.color_mode(py5.CMAP, self.paleta, 255)
            py5.no_stroke()
            cor = py5.remap(self.diametro, 0, DIAMETRO, 0, 255)
            b = py5.random_int(200, 205)
            py5.fill(cor, b)
            py5.translate(self.pos.x, self.pos.y, self.z)
            py5.circle(0, 0, self.diametro)

    def movimenta(self):
        """Aplica a velocidade à posição e prepara a velocidade do próximo quadro.

        A posição envolve nas bordas do canvas (módulo sobre ``width`` e
        ``height``), então quem sai de um lado reentra pelo oposto. A velocidade
        gira 2° por quadro no sentido da partícula e perde 0,5% do módulo — é
        essa combinação que fecha a trajetória numa espiral.
        """
        self.pos += self.velocidade
        self.pos.x %= py5.width
        self.pos.y %= py5.height
        self.velocidade.rotate(py5.radians(2) * self.sentido)
        self.velocidade *= 0.995


def inicializa():
    """Semeia a lista global ``particulas`` numa grade alternada de camadas.

    Cada célula da grade recebe :data:`REPETICOES` partículas, e cada repetição
    cai numa camada ``z`` própria — :data:`Z_BASE` mais :data:`PASSO_Z` por
    índice — de modo que a pilha ocupa profundidade em vez de se amontoar num
    plano só. A camada é herdada pelas filhas geradas na divisão.
    """
    largura, altura = helpers.DIMENSOES.external
    grade = cria_grade_ex(
        largura=largura,
        altura=altura,
        margem_x=0,
        margem_y=0,
        celula_x=PASSO,
        celula_y=PASSO,
        alternada=True,
    )
    for item in grade:
        x, y = item[1], item[3]
        for camada in range(REPETICOES):
            z = Z_BASE + camada * PASSO_Z
            particulas.append(Particula(x, y, z, diametro=DIAMETRO, paleta=cmap_paleta))


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.CMAP, cmap_paleta, 255)
    py5.background(py5.color(80))
    inicializa()


def draw():
    with py5.push():
        py5.translate(0, 0, -80)
        py5.fill(0, 10)
        for p in particulas.copy():
            p.atualiza()
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
