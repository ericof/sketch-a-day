"""2026-06-19
Caquinhos Redux 01
Homenagem aos pisos de caquinhos de São Paulo (Usando Voronoi).
ericof.com|https://bsky.app/profile/cefzanella.bsky.social/post/3mokxh3ae3s2o
png
Sketch,py5,CreativeCoding,Voronoi
"""

from opensimplex import OpenSimplex
from scipy.spatial import Voronoi
from sketches.utils.draw import canvas
from sketches.utils.draw.grade import cria_grade_ex
from sketches.utils.helpers import sketches as helpers

import math
import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0, 0, 0)
cor_fundo_interna = py5.color(60, 60, 45)

celula_x = 20
celula_y = 20
mult_x = 25
mult_y = 25
borda = 0.20
faixa_bagunca = 40

# Distancia do anel de sementes-sentinela alem da area interna. Precisa ser
# maior que o deslocamento maximo de uma semente interna (mult + faixa_bagunca)
# para que toda semente visivel fique cercada e sua celula seja finita.
margem_guarda = 100

noise_generator = OpenSimplex(seed=py5.random_int(20_000))

cacos: list[tuple[int, py5.Py5Shape]] = []


def par_bagunca(faixa_bagunca: int) -> tuple[float, float]:
    """Sorteia um deslocamento aleatorio em x e y dentro de uma faixa.

    :param faixa_bagunca: Amplitude maxima do deslocamento em cada eixo.
    :returns: Par ``(bx, by)`` de deslocamentos.
    """
    bx = py5.random(-faixa_bagunca, faixa_bagunca)
    by = py5.random(-faixa_bagunca, faixa_bagunca)
    return bx, by


def cor_caco(idx: int, idy: int) -> int:
    """Escolhe a cor de um caco a partir dos indices de grade da sua semente.

    :param idx: Indice da coluna na grade.
    :param idy: Indice da linha na grade.
    :returns: Cor do caco.
    """
    total = idx + idy
    cor = py5.color(152, 59, 47)
    if total % 10 == 0:
        cor = py5.color(0)
    elif total % 7 == 0:
        cor = py5.color(218, 160, 57)
    return cor


def gera_sementes(
    largura: int,
    altura: int,
    celula_x: int,
    celula_y: int,
) -> tuple[list[tuple[float, float]], list[tuple[int, int]], int]:
    """Gera as sementes do diagrama de Voronoi.

    As sementes internas vem de uma grade jitterada por noise e bagunca; em
    seguida um anel de sementes-sentinela e adicionado fora da area interna
    para garantir que toda celula visivel seja finita (fechada), dispensando
    o recorte das regioes abertas do Voronoi.

    :param largura: Largura da area interna.
    :param altura: Altura da area interna.
    :param celula_x: Passo horizontal da grade.
    :param celula_y: Passo vertical da grade.
    :returns: Tripla ``(pontos, indices, n_internas)`` onde as primeiras
        ``n_internas`` entradas de ``pontos`` sao as sementes visiveis e
        ``indices`` guarda o par ``(idx, idy)`` de cada uma para colorir.
    """
    pontos: list[tuple[float, float]] = []
    indices: list[tuple[int, int]] = []
    for idx, x0, idy, y0 in cria_grade_ex(
        largura, altura, 0, 0, celula_x, celula_y, True
    ):
        noise = noise_generator.noise2(x0, y0)
        bx, by = par_bagunca(faixa_bagunca)
        pontos.append((x0 + mult_x * noise + bx, y0 + mult_y * noise + by))
        indices.append((idx, idy))
    n_internas = len(pontos)

    passo = max(celula_x, celula_y)
    for c in range(-margem_guarda, largura + margem_guarda + 1, passo):
        pontos.append((c, -margem_guarda))
        pontos.append((c, altura + margem_guarda))
    for c in range(-margem_guarda, altura + margem_guarda + 1, passo):
        pontos.append((-margem_guarda, c))
        pontos.append((largura + margem_guarda, c))
    return pontos, indices, n_internas


def cria_forma_caco(verts: list[tuple[float, float]], cor: int) -> py5.Py5Shape:
    """Monta a forma de um caco a partir dos vertices da sua celula de Voronoi.

    Os vertices sao ordenados angularmente em torno do centroide (a celula e
    convexa, logo a ordem angular descreve o poligono simples) e entao
    encolhidos em direcao ao centroide pelo fator ``1 - borda``. A folga
    resultante entre cacos vizinhos revela o fundo, simulando o rejunte.

    :param verts: Vertices da celula de Voronoi.
    :param cor: Cor de preenchimento do caco.
    :returns: Forma pronta para ser desenhada.
    """
    cx = sum(v[0] for v in verts) / len(verts)
    cy = sum(v[1] for v in verts) / len(verts)
    verts = sorted(verts, key=lambda v: math.atan2(v[1] - cy, v[0] - cx))
    escala = 1 - borda
    forma = py5.create_shape()
    forma.set_fill(cor)
    forma.set_stroke_weight(0)
    with forma.begin_closed_shape():
        for vx, vy in verts:
            forma.vertex(cx + (vx - cx) * escala, cy + (vy - cy) * escala)
    return forma


def popula_cacos(
    largura: int,
    altura: int,
    celula_x: int,
    celula_y: int,
) -> list[tuple[int, py5.Py5Shape]]:
    """Constroi os cacos tesselando a area interna com um diagrama de Voronoi.

    :param largura: Largura da area interna.
    :param altura: Altura da area interna.
    :param celula_x: Passo horizontal da grade de sementes.
    :param celula_y: Passo vertical da grade de sementes.
    :returns: Lista de pares ``(z, forma)`` para desenho.
    """
    pontos, indices, n_internas = gera_sementes(largura, altura, celula_x, celula_y)
    vor = Voronoi(np.array(pontos))
    cacos = []
    for i in range(n_internas):
        regiao = vor.regions[vor.point_region[i]]
        if not regiao or -1 in regiao:
            # Celula aberta: nao deve ocorrer para sementes internas gracas ao
            # anel-sentinela, mas ignoramos por seguranca.
            continue
        verts = [tuple(vor.vertices[v]) for v in regiao]
        idx, idy = indices[i]
        forma = cria_forma_caco(verts, cor_caco(idx, idy))
        cacos.append((py5.random_int(0, 5), forma))
    return cacos


def inicializa():
    global cacos
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
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, -5)
        desenha_fundo(cor_fundo_interna)
        for z, forma in cacos:
            with py5.push():
                py5.translate(0, 0, z)
                py5.shape(forma)
    msg = (
        f"celula (x - y): {celula_x} - {celula_y} | "
        f"borda: {borda:.2f} | "
        f"bagunca: {faixa_bagunca}"
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
    global celula_x, celula_y, borda, faixa_bagunca
    key = py5.key
    match key:
        case "r":
            inicializa()
        case ">":
            celula_x += 2
            celula_y += 2
            inicializa()
        case "<":
            celula_x = max(4, celula_x - 2)
            celula_y = max(4, celula_y - 2)
            inicializa()
        case "w":
            borda = min(0.6, borda + 0.05)
            inicializa()
        case "s":
            borda = max(0.0, borda - 0.05)
            inicializa()
        case "+":
            faixa_bagunca += 5
            inicializa()
        case "-":
            faixa_bagunca = max(0, faixa_bagunca - 5)
            inicializa()
        case " ":
            save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
