"""2026-06-23
Caquinhos Redux 04
Pisos de caquinhos de São Paulo, realidade alternativa.
ericof.com
png
Sketch,py5,CreativeCoding,Voronoi
"""

from opensimplex import OpenSimplex
from random import shuffle
from scipy.spatial import Voronoi
from sketches.utils.draw import canvas
from sketches.utils.draw.grade import cria_grade_ex
from sketches.utils.helpers import sketches as helpers
from sketches.utils.helpers.timing import report_time

import math
import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0, 0, 0)
cor_fundo_interna = py5.color(60, 60, 45)

CORES_PESOS = (
    (py5.color("#A66A2C"), 93),
    (py5.color("#B17534"), 5),
    (py5.color("#CF964B"), 2),
)

celula_x = 20
celula_y = 20
mult_x = 15
mult_y = 15
borda = 0.15
faixa_bagunca = 20
profundidade_caco = 12

# Ponto de luz controlado pelo mouse: x,y vem do cursor, altura (z) e tom sao
# fixos. A ambiente baixa evita que os cacos longe da luz fiquem pretos.
luz_altura = 600
luz_cor = py5.color(255, 244, 214)
luz_ambiente = py5.color(40, 40, 40)

# Distancia do anel de sementes-sentinela alem da area interna. Precisa ser
# maior que o deslocamento maximo de uma semente interna (mult + faixa_bagunca)
# para que toda semente visivel fique cercada e sua celula seja finita.
margem_guarda = 100

noise_generator = OpenSimplex(seed=py5.random_int(20_000))

cacos: list[py5.Py5Shape] = []


def cores_pesos() -> list[int]:
    """Expande ``CORES_PESOS`` numa lista com cada cor repetida conforme seu peso.

    A lista e embaralhada e serve de base para o sorteio ponderado de cores
    em :func:`cor_caco`.

    :returns: Lista de cores com repeticao proporcional ao peso de cada uma.
    """
    cores = []
    for cor, peso in CORES_PESOS:
        cores.extend([cor] * peso)
    shuffle(cores)
    return cores


CORES = cores_pesos()


def par_bagunca(faixa_bagunca: int) -> tuple[float, float]:
    """Sorteia um deslocamento aleatorio em x e y dentro de uma faixa.

    :param faixa_bagunca: Amplitude maxima do deslocamento em cada eixo.
    :returns: Par ``(bx, by)`` de deslocamentos.
    """
    bx = py5.random(-faixa_bagunca, faixa_bagunca)
    by = py5.random(-faixa_bagunca, faixa_bagunca)
    return bx, by


def cor_caco() -> int:
    """Sorteia a cor de um caco com probabilidade proporcional aos pesos.

    O sorteio e feito sobre ``CORES`` (a lista expandida por :func:`cores_pesos`),
    de modo que cada cor aparece na frequencia definida em ``CORES_PESOS``.

    :returns: Cor do caco.
    """
    return py5.random_choice(CORES)


def gera_sementes(
    largura: int,
    altura: int,
    celula_x: int,
    celula_y: int,
) -> tuple[list[tuple[float, float]], int]:
    """Gera as sementes do diagrama de Voronoi.

    As sementes internas vem de uma grade jitterada por noise e bagunca; em
    seguida um anel de sementes-sentinela e adicionado fora da area interna
    para garantir que toda celula visivel seja finita (fechada), dispensando
    o recorte das regioes abertas do Voronoi.

    :param largura: Largura da area interna.
    :param altura: Altura da area interna.
    :param celula_x: Passo horizontal da grade.
    :param celula_y: Passo vertical da grade.
    :returns: Par ``(pontos, n_internas)`` onde as primeiras ``n_internas``
        entradas de ``pontos`` sao as sementes visiveis e o restante e o
        anel-sentinela.
    """
    pontos: list[tuple[float, float]] = []
    for _, x0, _, y0 in cria_grade_ex(largura, altura, 0, 0, celula_x, celula_y, True):
        noise = noise_generator.noise2(x0, y0)
        bx, by = par_bagunca(faixa_bagunca)
        pontos.append((x0 + mult_x * noise + bx, y0 + mult_y * noise + by))
    n_internas = len(pontos)

    passo = max(celula_x, celula_y)
    for c in range(-margem_guarda, largura + margem_guarda + 1, passo):
        pontos.append((c, -margem_guarda))
        pontos.append((c, altura + margem_guarda))
    for c in range(-margem_guarda, altura + margem_guarda + 1, passo):
        pontos.append((-margem_guarda, c))
        pontos.append((largura + margem_guarda, c))
    return pontos, n_internas


def cria_forma_caco(verts: list[tuple[float, float]], cor: int) -> py5.Py5Shape:
    """Monta o prisma 3D de um caco a partir da sua celula de Voronoi.

    Os vertices sao ordenados angularmente em torno do centroide (a celula e
    convexa, logo a ordem angular descreve o poligono simples) e encolhidos em
    direcao ao centroide pelo fator ``1 - borda`` -- a folga entre cacos
    vizinhos revela o fundo, simulando o rejunte. O poligono resultante e
    extrudado em ``profundidade_caco`` ao longo de z: a base fica em ``z = 0``
    (assentada no fundo) e o topo em ``z = profundidade_caco`` (voltado para a
    camera).

    A forma e um ``GROUP`` com uma sub-forma por face -- topo mais uma parede
    por aresta --, cada uma com sua propria ``normal()`` para que a iluminacao
    incida corretamente (uma unica ``normal()`` vale por ``Py5Shape``).

    :param verts: Vertices da celula de Voronoi.
    :param cor: Cor de preenchimento do caco.
    :returns: ``GROUP`` com as faces do prisma, pronto para ser desenhado.
    """
    cx = sum(v[0] for v in verts) / len(verts)
    cy = sum(v[1] for v in verts) / len(verts)
    verts = sorted(verts, key=lambda v: math.atan2(v[1] - cy, v[0] - cx))
    escala = 1 - borda
    pts = [(cx + (vx - cx) * escala, cy + (vy - cy) * escala) for vx, vy in verts]

    grupo = py5.create_shape(py5.GROUP)

    # Topo: face voltada para a camera (normal +z), no nivel z = profundidade.
    topo = py5.create_shape()
    topo.set_fill(cor)
    topo.set_stroke_weight(0)
    with topo.begin_closed_shape():
        topo.normal(0, 0, 1)
        for px, py_ in pts:
            topo.vertex(px, py_, profundidade_caco)
    grupo.add_child(topo)

    # Paredes: uma face por aresta, ligando a base (z=0) ao topo (z=prof).
    n = len(pts)
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        dx, dy = x1 - x0, y1 - y0
        comp = math.hypot(dx, dy) or 1.0
        nx, ny = dy / comp, -dx / comp  # normal externa, no plano xy
        parede = py5.create_shape()
        parede.set_fill(cor)
        parede.set_stroke_weight(0)
        with parede.begin_closed_shape():
            parede.normal(nx, ny, 0)
            parede.vertex(x0, y0, 0)
            parede.vertex(x1, y1, 0)
            parede.vertex(x1, y1, profundidade_caco)
            parede.vertex(x0, y0, profundidade_caco)
        grupo.add_child(parede)
    return grupo


def popula_cacos(
    largura: int,
    altura: int,
    celula_x: int,
    celula_y: int,
) -> list[py5.Py5Shape]:
    """Constroi os cacos tesselando a area interna com um diagrama de Voronoi.

    :param largura: Largura da area interna.
    :param altura: Altura da area interna.
    :param celula_x: Passo horizontal da grade de sementes.
    :param celula_y: Passo vertical da grade de sementes.
    :returns: Lista de prismas (``GROUP``) prontos para desenho.
    """
    pontos, n_internas = gera_sementes(largura, altura, celula_x, celula_y)
    vor = Voronoi(np.array(pontos))
    cacos = []
    for i in range(n_internas):
        regiao = vor.regions[vor.point_region[i]]
        if not regiao or -1 in regiao:
            # Celula aberta: nao deve ocorrer para sementes internas gracas ao
            # anel-sentinela, mas ignoramos por seguranca.
            continue
        verts = [tuple(vor.vertices[v]) for v in regiao]
        cacos.append(cria_forma_caco(verts, cor_caco()))
    return cacos


def inicializa():
    global cacos
    with report_time("Calculando..."):
        cacos = popula_cacos(*helpers.DIMENSOES.internal, celula_x, celula_y)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    inicializa()


def desenha_fundo(cor: int):
    """Desenha o fundo por baixo dos caquinhos."""
    with py5.push():
        py5.fill(cor)
        py5.no_stroke()
        py5.rect(0, 0, *helpers.DIMENSOES.internal)


def draw():
    py5.background(cor_fundo)
    # Posicao da luz no espaco interno: o mouse e screen-space, entao
    # descontamos a origem do painel (pos_interno).
    luz_x = py5.mouse_x - helpers.DIMENSOES.pos_interno[0]
    luz_y = py5.mouse_y - helpers.DIMENSOES.pos_interno[1]
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, -15)
        # Fundo desenhado antes das luzes para manter o rejunte chapado; os
        # prismas se assentam nele (base em z=0) e sobem em direcao a camera.
        desenha_fundo(cor_fundo_interna)
        # Luz pontual seguindo o mouse + ambiente baixa, posicionadas no mesmo
        # espaco dos cacos. Atuam so aqui; o no_lights() abaixo protege o frame.
        py5.ambient_light(
            py5.red(luz_ambiente), py5.green(luz_ambiente), py5.blue(luz_ambiente)
        )
        py5.point_light(
            py5.red(luz_cor),
            py5.green(luz_cor),
            py5.blue(luz_cor),
            luz_x,
            luz_y,
            luz_altura,
        )
        for forma in cacos:
            py5.shape(forma)
    # Apaga as luzes antes do overlay 2D para nao lavar o frame/creditos.
    py5.no_lights()
    msg = (
        f"celula (x - y): {celula_x} - {celula_y} | "
        f"borda: {borda:.2f} | "
        f"bagunca: {faixa_bagunca} | "
        f"prof: {profundidade_caco} | "
        f"luz (x - y): {luz_x} - {luz_y}"
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
    global celula_x, celula_y, borda, faixa_bagunca, profundidade_caco
    key = py5.key
    match key:
        case "r":
            inicializa()
        case ">" | "<":
            passo = 2 if key == ">" else -2
            celula_x = max(4, celula_x + passo)
            celula_y = max(4, celula_y + passo)
            inicializa()
        case "w" | "s":
            borda = min(0.6, max(0.0, borda + (0.05 if key == "w" else -0.05)))
            inicializa()
        case "+" | "-":
            faixa_bagunca = max(0, faixa_bagunca + (5 if key == "+" else -5))
            inicializa()
        case "e" | "d":
            profundidade_caco = max(0, profundidade_caco + (1 if key == "e" else -1))
            inicializa()
        case " ":
            save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
