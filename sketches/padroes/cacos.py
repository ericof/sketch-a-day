from opensimplex import OpenSimplex
from scipy.spatial import Voronoi

import math
import numpy as np
import py5


def gera_sementes(
    largura: int,
    altura: int,
    celula_x: int,
    celula_y: int,
    grade: list[tuple[float, float]],
    mult_x: float,
    mult_y: float,
    faixa_bagunca: int,
    margem_guarda: int,
    noise_generator: OpenSimplex,
) -> tuple[list[tuple[float, float]], int]:
    """Gera as sementes do diagrama de Voronoi.

    As sementes internas vem de uma grade jitterada por noise e bagunca; em
    seguida um anel de sementes-sentinela e adicionado fora da area interna
    para garantir que toda celula visivel seja finita (fechada), dispensando
    o recorte das regioes abertas do Voronoi.

    :param largura: Largura da area a tesselar.
    :param altura: Altura da area a tesselar.
    :param celula_x: Passo horizontal usado no espacamento do anel-sentinela.
    :param celula_y: Passo vertical usado no espacamento do anel-sentinela.
    :param grade: Pontos ``(x, y)`` da grade base das sementes internas.
    :param mult_x: Amplitude do deslocamento por noise no eixo x.
    :param mult_y: Amplitude do deslocamento por noise no eixo y.
    :param faixa_bagunca: Amplitude do deslocamento aleatorio (bagunca) por eixo.
    :param margem_guarda: Distancia do anel-sentinela alem da area a tesselar.
    :param noise_generator: Gerador OpenSimplex que jittera as sementes internas.
    :returns: Par ``(pontos, n_internas)`` onde as primeiras ``n_internas``
        entradas de ``pontos`` sao as sementes visiveis e o restante e o
        anel-sentinela.
    """
    pontos: list[tuple[float, float]] = []
    for x0, y0 in grade:
        noise = noise_generator.noise2(x0, y0)
        bx = py5.random(-faixa_bagunca, faixa_bagunca)
        by = py5.random(-faixa_bagunca, faixa_bagunca)
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


def cria_forma_caco(
    verts: list[tuple[float, float]], cor: int, borda: float, profundidade_caco: float
) -> py5.Py5Shape:
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
    :param borda: Fracao de encolhimento da celula rumo ao centroide (rejunte).
    :param profundidade_caco: Altura da extrusao do prisma ao longo de z.
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
    grade: list[tuple[float, float]],
    mult_x: float,
    mult_y: float,
    faixa_bagunca: int,
    margem_guarda: int,
    borda: float,
    profundidade_caco: float,
    noise_generator: OpenSimplex,
    cores: list[int],
) -> list[py5.Py5Shape]:
    """Constroi os cacos tesselando a area interna com um diagrama de Voronoi.

    :param largura: Largura da area a tesselar.
    :param altura: Altura da area a tesselar.
    :param celula_x: Passo horizontal do anel-sentinela (repassado a
        :func:`gera_sementes`).
    :param celula_y: Passo vertical do anel-sentinela (repassado a
        :func:`gera_sementes`).
    :param grade: Pontos ``(x, y)`` da grade base das sementes internas.
    :param mult_x: Amplitude do deslocamento por noise no eixo x.
    :param mult_y: Amplitude do deslocamento por noise no eixo y.
    :param faixa_bagunca: Amplitude do deslocamento aleatorio (bagunca) por eixo.
    :param margem_guarda: Distancia do anel-sentinela alem da area a tesselar.
    :param borda: Fracao de encolhimento de cada caco rumo ao centroide (rejunte).
    :param profundidade_caco: Altura da extrusao dos prismas ao longo de z.
    :param noise_generator: Gerador OpenSimplex que jittera as sementes internas.
    :param cores: Cores candidatas para o sorteio ponderado de cada caco.
    :returns: Lista de prismas (``GROUP``) prontos para desenho.
    """
    pontos, n_internas = gera_sementes(
        largura,
        altura,
        celula_x,
        celula_y,
        grade,
        mult_x,
        mult_y,
        faixa_bagunca,
        margem_guarda,
        noise_generator,
    )
    vor = Voronoi(np.array(pontos))
    cacos = []
    for i in range(n_internas):
        cor = py5.random_choice(cores)
        regiao = vor.regions[vor.point_region[i]]
        if not regiao or -1 in regiao:
            # Celula aberta: nao deve ocorrer para sementes internas gracas ao
            # anel-sentinela, mas ignoramos por seguranca.
            continue
        verts = [tuple(vor.vertices[v]) for v in regiao]
        cacos.append(cria_forma_caco(verts, cor, borda, profundidade_caco))
    return cacos
