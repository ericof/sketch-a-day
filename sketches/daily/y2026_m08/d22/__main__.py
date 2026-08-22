"""2026-08-22
Tunnel of Boxes 06
Inspirado no sketch de Alexandre Villares, lembrança de Túnel do Tempo.
ericof.com|https://github.com/villares/sketch-a-day/tree/main/2026/sketch_2026_08_15
png
Sketch,py5,CreativeCoding,abav
"""

from collections import deque
from itertools import pairwise
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
semente: int = 26876
lados: int = 40
profundidade: int = 900
passo: int = 60
raio: int = 500
p_raio = (profundidade * 2) / passo
z_inicial: int = -460
buffer_x: int = 0
buffer_y: int = -120


SEGMENTOS_CONE: int = 24
# Amplitude do giro comandado pelo mouse, em graus para cada lado do centro.
ROTACAO_MAX: float = 15
SEGMENTOS_PAREDE: int = 100
FOLGA_PAREDE: float = 15
# Cinza neutro: definido fora do color_mode(HSB) do setup, então um único
# argumento é o jeito seguro de pedir cinza — vale em RGB e em HSB.
COR_PAREDE = py5.color(90)
# 40% de opacidade. O color_mode(HSB, 360, 100, 100) do setup passa três máximos
# e não toca no do alfa, que segue na escala padrão de 255.
ALFA_PAREDE: float = 255 * 0.1


PALETAS: tuple[str, ...] = (
    "op-1726494-01",
    "bright-colors",
    "south-africa",
    "op-1726494-01",
)


def caixa(
    x: float,
    y: float,
    z: float,
    w: float,
    h: float | None = None,
    d: float | None = None,
    rot_x: float = 0,
    rot_y: float = 0,
    rot_z: float = 0,
) -> None:
    """Desenha uma caixa posicionada e rotacionada, sem vazar transformações.

    Envolve :func:`py5.box` — que sempre desenha na origem do sistema de
    coordenadas corrente — numa matriz própria, de modo que a translação e as
    rotações valem só para esta caixa e o chamador continua no mesmo referencial
    de antes.

    As rotações são aplicadas na ordem x, y, z **após** a translação, então giram
    a caixa em torno do próprio centro, não em torno da origem da cena.

    Omitir ``h`` e ``d`` produz um cubo: ambos assumem o valor de ``w``.

    :param x: posição no eixo x, relativa ao referencial corrente.
    :param y: posição no eixo y, relativa ao referencial corrente.
    :param z: posição no eixo z, relativa ao referencial corrente.
    :param w: largura da caixa; serve de padrão para ``h`` e ``d``.
    :param h: altura da caixa; ``None`` copia ``w``.
    :param d: profundidade da caixa; ``None`` copia ``w``.
    :param rot_x: rotação em torno do eixo x, em radianos.
    :param rot_y: rotação em torno do eixo y, em radianos.
    :param rot_z: rotação em torno do eixo z, em radianos.
    """
    h = w if h is None else h
    d = w if d is None else d
    with py5.push():
        py5.translate(x, y, z)
        py5.rotate_x(rot_x)
        py5.rotate_y(rot_y)
        py5.rotate_z(rot_z)
        py5.box(w, h, d)


def cone(
    x: float,
    y: float,
    z: float,
    w: float,
    h: float | None = None,
    d: float | None = None,
    rot_x: float = 0,
    rot_y: float = 0,
    rot_z: float = 0,
) -> None:
    """Desenha um cone posicionado e rotacionado, sem vazar transformações.

    Mesma assinatura e mesmas convenções de :func:`caixa`: o cone é inscrito na
    caixa de dimensões ``w x h x d``, centrado na origem local, com a base
    elíptica (raios ``w/2`` e ``d/2``) em ``y = h/2`` e o ápice em ``y = -h/2``
    — ou seja, apontando para o mesmo lado que ``rot_z`` orienta.

    Como :func:`py5` não traz uma primitiva de cone, a malha é construída à mão
    com ``SEGMENTOS_CONE`` fatias: um leque de triângulos para a superfície
    lateral e outro para a tampa da base. Cada triângulo lateral emite sua
    própria normal (produto vetorial da aresta da base pela aresta que sobe ao
    ápice, normalizado), porque em P3D uma face sem ``normal()`` não responde a
    nenhuma luz — renderiza chapada.

    Omitir ``h`` e ``d`` produz um cone de base circular com altura igual ao
    diâmetro: ambos assumem o valor de ``w``.

    :param x: posição no eixo x, relativa ao referencial corrente.
    :param y: posição no eixo y, relativa ao referencial corrente.
    :param z: posição no eixo z, relativa ao referencial corrente.
    :param w: largura da base; serve de padrão para ``h`` e ``d``.
    :param h: altura do cone, da base ao ápice; ``None`` copia ``w``.
    :param d: profundidade da base; ``None`` copia ``w``.
    :param rot_x: rotação em torno do eixo x, em radianos.
    :param rot_y: rotação em torno do eixo y, em radianos.
    :param rot_z: rotação em torno do eixo z, em radianos.
    """
    h = w if h is None else h
    d = w if d is None else d
    raio_x = w / 2
    raio_z = d / 2
    base = h / 2
    topo = -h / 2
    passo_ang = py5.TAU / SEGMENTOS_CONE
    anel = [
        (
            float(raio_x * py5.cos(i * passo_ang)),
            float(raio_z * py5.sin(i * passo_ang)),
        )
        for i in range(SEGMENTOS_CONE + 1)
    ]
    with py5.push():
        py5.translate(x, y, z)
        py5.rotate_x(rot_x)
        py5.rotate_y(rot_y)
        py5.rotate_z(rot_z)
        with py5.begin_shape(py5.TRIANGLES):
            for (x0, z0), (x1, z1) in pairwise(anel):
                nx = (z1 - z0) * h
                ny = (x1 - x0) * z0 - (z1 - z0) * x0
                nz = -(x1 - x0) * h
                norma = float(py5.sqrt(nx * nx + ny * ny + nz * nz)) or 1.0
                py5.normal(nx / norma, ny / norma, nz / norma)
                py5.vertex(x0, base, z0)
                py5.vertex(x1, base, z1)
                py5.vertex(0, topo, 0)
        with py5.begin_shape(py5.TRIANGLE_FAN):
            py5.normal(0, 1, 0)
            py5.vertex(0, base, 0)
            for x0, z0 in anel:
                py5.vertex(x0, base, z0)


def raio_do_anel(idz: int) -> float:
    """Raio do túnel na fatia de profundidade ``idz``.

    O túnel não é um cilindro: o raio cresce de 20% a 80% de ``raio`` conforme a
    fatia avança de ``-profundidade`` até ``+profundidade``, o que produz o
    afunilamento em direção ao fundo. Fonte única do raio para :func:`draw` — que
    posiciona os cones — e :func:`parede`, que os envolve; se cada um recalculasse
    o afunilamento por conta própria, os dois divergiriam ao primeiro ajuste.

    :param idz: índice da fatia, de ``0`` a ``p_raio``.
    :returns: raio em pixels, no referencial do túnel.
    """
    return float(py5.remap(idz / p_raio, 0, 1, 0.6, 0.8) * raio)


def parede() -> None:
    """Desenha a parede cilíndrica de onde os cones parecem se projetar.

    É um tubo aberto construído como uma sequência de ``QUAD_STRIP``, um por par
    de fatias consecutivas, seguindo o mesmo afunilamento de :func:`raio_do_anel`
    acrescido de ``FOLGA_PAREDE`` — folga suficiente para engolir a base do cone
    mais alto sorteado, de modo que só as pontas apareçam para dentro do túnel.

    As normais apontam para **dentro**, já que é a face interna que a câmera vê.
    Para a superfície ``P(a, z) = (R sin a, R cos a, z)``, a normal interna vale
    ``(-sin a, -cos a, dR/dz)`` — a componente em z é o que faz o afunilamento
    responder às luzes em vez de parecer um cilindro reto.

    O tubo é desenhado sem contorno: com ``stroke`` ativo, as arestas dos strips
    virariam uma malha de arame sobre o cinza.
    """
    passo_ang = py5.TAU / SEGMENTOS_PAREDE
    angulos = [i * passo_ang for i in range(SEGMENTOS_PAREDE + 1)]
    faixas = [
        (float(z), raio_do_anel(idz) + FOLGA_PAREDE)
        for idz, z in enumerate(range(-profundidade, profundidade + passo, passo))
    ]
    py5.fill(COR_PAREDE, ALFA_PAREDE)
    py5.no_stroke()
    for (z0, r0), (z1, r1) in pairwise(faixas):
        inclinacao = (r1 - r0) / (z1 - z0)
        norma = (1 + inclinacao * inclinacao) ** 0.5
        with py5.begin_shape(py5.QUAD_STRIP):
            for a in angulos:
                x0 = float(r0 * py5.sin(a))
                y0 = float(r0 * py5.cos(a))
                py5.normal(-x0 / r0 / norma, -y0 / r0 / norma, inclinacao / norma)
                py5.vertex(x0, y0, z0)
                py5.vertex(float(r1 * py5.sin(a)), float(r1 * py5.cos(a)), z1)


def nova_semente() -> int:
    """Sorteia uma semente para o gerador pseudoaleatório do sketch.

    Usada pela tecla ``r`` para trocar a configuração do túnel: o ``draw()``
    chama :func:`py5.random_seed` com a semente a cada quadro, então todo o
    sorteio de tamanhos das caixas é determinístico e uma nova semente redesenha
    o túnel inteiro de outro jeito.

    Note que a semente vem do próprio :func:`py5.random`, que acabou de ser
    reinicializado pela semente anterior — a sequência de sementes é, ela
    mesma, reprodutível a partir da primeira.

    :returns: inteiro no intervalo ``[0, 1000000)``.
    """
    return int(py5.random(1000000))


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.frame_rate(10)


def draw() -> None:
    py5.background(cor_fundo)
    graus_y = float(
        py5.constrain(
            py5.remap(py5.mouse_x, 0, py5.width, -ROTACAO_MAX, ROTACAO_MAX),
            -ROTACAO_MAX,
            ROTACAO_MAX,
        )
    )
    rotacao_y = float(py5.radians(graus_y))
    paletas: deque[deque] = deque(gera_paleta(p, True) for p in PALETAS)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, z_inicial)
        py5.directional_light(360, 0, 100, 0, 0, 100)
        py5.directional_light(360, 0, 100, 0, 0, -100)
        py5.directional_light(360, 0, 100, 100, 100, 100)
        py5.random_seed(semente)
        cx = py5.width / 2 + buffer_x
        cy = py5.height / 2 + buffer_y
        py5.translate(cx, cy)
        py5.rotate_y(rotacao_y)
        espacamento = 360 / lados
        parede()
        for i in range(lados):
            for idz, z_base in enumerate(range(-profundidade, profundidade, passo)):
                z = z_base - 100
                forma = caixa if (i + idz) % 3 == 0 else cone
                paleta = paletas[(idz + i) % len(paletas)]
                mult_t = py5.remap((idz / p_raio), 0, 1, 0.75, 0.9)
                r = raio_do_anel(idz)
                cor = int(paleta[0])
                # Anéis pares entram meio passo defasados: os cones de um anel
                # caem na fresta do anel vizinho, em vez de alinhar colunas.
                defasagem = espacamento / 2 if idz % 2 == 0 else 0
                a = float(py5.radians(i * espacamento + defasagem))
                x = float(r * py5.sin(a))
                y = float(r * py5.cos(a))
                tamanho = float(py5.random(5, 40) * mult_t)
                altura = float(py5.random(0.5, 2) * tamanho)
                py5.fill(cor)
                py5.stroke(cor)
                paleta.rotate(1)
                forma(x, y, z, tamanho, altura, rot_z=-a)

    msg = (
        f"Semente: {semente} | Rotação Y: {graus_y:.1f}° | "
        f"Buffer X: {buffer_x} | Buffer Y: {buffer_y} | Lados: {lados}"
    )
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
        msg=msg,
    )


def key_pressed():
    global semente, lados, buffer_x, buffer_y
    key = py5.key
    match key:
        case "w":
            buffer_y -= 1
        case "s":
            buffer_y += 1
        case "d":
            buffer_x += 1
        case "a":
            buffer_x -= 1
        case "-":
            lados -= 1 if lados > 1 else 0
        case "+":
            lados += 1
        case " ":
            save_and_close()
        case "r":
            semente = nova_semente()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
