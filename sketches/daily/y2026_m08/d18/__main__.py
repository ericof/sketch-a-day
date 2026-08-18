"""2026-08-18
Tunnel of Boxes 02
Inspirado no sketch de Alexandre Villares, lembrança de Túnel do Tempo.
ericof.com|https://github.com/villares/sketch-a-day/tree/main/2026/sketch_2026_08_15
png
Sketch,py5,CreativeCoding,abav
"""

from collections import deque
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
semente: int = 26876
lados: int = 40
profundidade: int = 800
passo: int = 60
raio: int = 600
p_raio = (profundidade * 2) / passo
z_inicial: int = -850
buffer_x: int = 120
buffer_y: int = -108


PALETAS: tuple[str, ...] = (
    "Warhol",
    "bright-colors",
    "pastel",
    "south-africa",
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
    rotacao_y = py5.radians(py5.mouse_x)
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
        for i in range(lados):
            for idz, z in enumerate(range(-profundidade, profundidade, passo)):
                paleta = paletas[idz % len(paletas)]
                mult_r = py5.remap((idz / p_raio), 0, 1, 0.2, 0.8)
                mult_t = py5.remap((idz / p_raio), 0, 1, 0.75, 0.9)
                r = mult_r * raio
                cor = int(paleta[0])
                a = float(py5.radians(i * espacamento))
                x = float(r * py5.sin(a))
                y = float(r * py5.cos(a))
                tamanho = float(py5.random(5, 40) * mult_t)
                altura = float(py5.random(0.5, 2) * tamanho)
                py5.fill(cor)
                paleta.rotate(1)
                caixa(x, y, z, tamanho, altura, rot_z=-a)

    msg = (
        f"Semente: {semente} | Rotação Y: {rotacao_y:.2f} | "
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
