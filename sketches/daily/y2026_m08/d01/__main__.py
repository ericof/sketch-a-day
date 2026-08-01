"""2026-08-01
Formas Geométricas Redux 08
Exercício de grade de formas geométricas
ericof.com|https://ericof.com/en/sketches/2024-06-29
png
Sketch,py5,CreativeCoding,Vornoi
"""

from opensimplex import OpenSimplex
from scipy.spatial import Voronoi
from shapely import make_valid
from shapely.geometry import Polygon
from sketches.padroes.cacos import gera_sementes
from sketches.padroes.poligonos import vertices_poligono_regular
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.grade import cria_grade_ex
from sketches.utils.helpers import sketches as helpers

import math
import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

celula_x: int = 80
celula_y: int = 20
# Escala aplicada ao poligono antes do recorte. Ate ~0.9 o poligono cabe
# inteiro na sua celula (aparecem folgas); a partir de ~1.0 ele transborda e e
# recortado na fronteira de Voronoi, fazendo formas vizinhas compartilharem a
# aresta -- e ai que elas "se interseccionam". ~1.15 mantem o caráter do
# poligono e ja recorta as sobreposicoes.
forma_escala: float = 5.50
alternada: bool = True
preencher: bool = True

# Lados dos poligonos sorteados por posicao (indice (idx + idy) na grade).
LADOS: tuple[int, ...] = (8, 6, 8, 6, 6, 7, 8, 5, 7, 8, 9)

# Jitter opcional das sementes (0 = mosaico geometrico limpo; aumente para
# celulas organicas). mult desloca por noise; bagunca desloca aleatoriamente.
jitter_mult: float = 40.0
jitter_bagunca: int = 6

# Distancia do anel de sementes-sentinela alem da area visivel. Precisa superar
# o deslocamento maximo de uma semente (jitter_mult + jitter_bagunca) para que
# toda celula visivel fique fechada e o recorte nunca falhe por celula aberta.
margem_guarda: int = 300

traco: float = 3.4
cor_traco_preenchido = py5.color(0, 0, 0, 0.8)
traco_preenchido: float = 1.5

# Extrusao 3D: cada forma 2D vira um tronco (base cheia + topo elevado e menor).
# A camera P3D e frontal, entao e a reducao do topo -- e nao a altura sozinha --
# que revela as paredes/bisel e faz nascer o volume. altura desloca o topo em z
# na direcao da camera; reducao_topo encolhe o topo em torno do centroide;
# sombra_parede escurece as paredes rumo ao fundo para o relevo se ler.
altura: float = 120.0
reducao_topo: float = 0.75
sombra_parede: float = 0.1

noise_generator = OpenSimplex(seed=py5.random_int(20_000))

formas: list[py5.Py5Shape] = []


def celula_como_poligono(vor: Voronoi, indice: int) -> Polygon | None:
    """Extrai a celula de Voronoi de uma semente como poligono shapely.

    A regiao de Voronoi devolve os vertices sem ordem garantida; como a celula e
    convexa, ordena-los angularmente em torno do centroide descreve o poligono
    simples. Sementes internas sempre tem celula fechada gracas ao anel-sentinela.

    :param vor: Diagrama de Voronoi ja calculado.
    :param indice: Indice da semente em ``vor.point_region``.
    :returns: A celula como :class:`~shapely.geometry.Polygon` valida, ou
        ``None`` se a regiao for aberta/degenerada.
    """
    regiao = vor.regions[vor.point_region[indice]]
    if not regiao or -1 in regiao:
        return None
    verts = [tuple(vor.vertices[v]) for v in regiao]
    cx = sum(v[0] for v in verts) / len(verts)
    cy = sum(v[1] for v in verts) / len(verts)
    verts.sort(key=lambda v: math.atan2(v[1] - cy, v[0] - cx))
    return make_valid(Polygon(verts))


def poligono_na_semente(cx: float, cy: float, lados: int) -> Polygon:
    """Constroi o poligono regular escalado, centrado na semente.

    Os vertices vem centrados em ``(tam / 2, tam / 2)``; sao transladados para a
    origem e reposicionados em ``(cx, cy)`` para casar com a celula (que vive em
    coordenadas absolutas).

    :param cx: Coordenada x do centro (a semente).
    :param cy: Coordenada y do centro (a semente).
    :param lados: Numero de lados do poligono regular.
    :returns: O poligono regular escalado como :class:`~shapely.geometry.Polygon`.
    """
    tam_x = celula_x * forma_escala
    tam_y = celula_y * forma_escala
    verts = vertices_poligono_regular(tam_x, tam_y, lados)
    verts = verts - [tam_x / 2, tam_y / 2] + [cx, cy]
    return make_valid(Polygon(verts))


def forma_extrudada(geom) -> py5.Py5Shape | None:
    """Extruda a interseccao poligono-celula num tronco 3D (base + topo elevado).

    A interseccao de dois convexos e um unico poligono convexo; ainda assim
    tratamos ``MultiPolygon`` / ``GeometryCollection`` por seguranca, tomando o
    maior anel. A partir do anel-base (``z = 0``) gera-se um anel-topo elevado em
    ``altura`` e encolhido por ``reducao_topo`` em torno do centroide; as paredes
    laterais (um ``Py5Shape`` por aresta) ligam base e topo, e uma tampa fecha o
    conjunto. O ``GROUP`` resultante e colorido no ``draw`` (tampa cheia, paredes
    escurecidas). Retorna ``None`` quando nada sobra (poligono fora da celula).

    :param geom: Geometria shapely resultante do ``intersection``.
    :returns: O tronco como ``GROUP`` de faces em coordenadas absolutas, ou
        ``None`` se vazia/degenerada.
    """
    if geom.is_empty:
        return None
    if geom.geom_type == "Polygon":
        maior = geom
    else:
        poligonos = [g for g in getattr(geom, "geoms", []) if g.geom_type == "Polygon"]
        if not poligonos:
            return None
        maior = max(poligonos, key=lambda g: g.area)

    anel = list(maior.exterior.coords[:-1])
    if len(anel) < 3:
        return None
    cx = sum(x for x, _ in anel) / len(anel)
    cy = sum(y for _, y in anel) / len(anel)
    base = [(x, y, 0.0) for x, y in anel]
    topo = [
        (cx + reducao_topo * (x - cx), cy + reducao_topo * (y - cy), altura)
        for x, y in anel
    ]

    grupo = py5.create_shape(py5.GROUP)
    n = len(anel)
    for i in range(n):
        j = (i + 1) % n
        parede = py5.create_shape()
        with parede.begin_closed_shape():
            parede.vertex(*base[i])
            parede.vertex(*base[j])
            parede.vertex(*topo[j])
            parede.vertex(*topo[i])
        grupo.add_child(parede)

    tampa = py5.create_shape()
    with tampa.begin_closed_shape():
        for vertice in topo:
            tampa.vertex(*vertice)
    grupo.add_child(tampa)
    return grupo


def inicializa():
    global formas
    grade_ex = cria_grade_ex(
        *helpers.DIMENSOES.external, 0, 0, celula_x, celula_y, alternada=alternada
    )
    grade = [(x, y) for _, x, _, y in grade_ex]
    lados_por_semente = [LADOS[(idx + idy) % len(LADOS)] for idx, _, idy, _ in grade_ex]

    pontos, n_internas = gera_sementes(
        *helpers.DIMENSOES.external,
        celula_x,
        celula_y,
        grade,
        jitter_mult,
        jitter_mult,
        jitter_bagunca,
        margem_guarda,
        noise_generator,
    )
    vor = Voronoi(np.array(pontos))

    formas = []
    for i in range(n_internas):
        celula = celula_como_poligono(vor, i)
        if celula is None:
            continue
        cx, cy = pontos[i]
        poligono = poligono_na_semente(cx, cy, lados_por_semente[i])
        forma = forma_extrudada(poligono.intersection(celula))
        if forma is not None:
            formas.append(forma)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    inicializa()


def estiliza(forma: py5.Py5Shape, cor) -> None:
    """Aplica cor e traco as faces de um tronco extrudado e o desenha.

    Percorre as faces do ``GROUP``: as paredes (todas menos a ultima) recebem
    ``cor`` escurecida rumo ao fundo por ``sombra_parede``, para o relevo se ler;
    a tampa (ultima face) recebe ``cor`` cheia. Em modo contorno (``preencher``
    falso) todas as faces ficam so com traco em ``cor``.

    :param forma: O ``GROUP`` de faces (paredes + tampa) a estilizar.
    :param cor: A cor base da forma (entrada corrente da paleta).
    """
    n = forma.get_child_count()
    cor_parede = py5.lerp_color(cor, cor_fundo, sombra_parede)
    for i in range(n):
        filho = forma.get_child(i)
        if preencher:
            filho.set_fill(cor_parede if i < n - 1 else cor)
            filho.set_stroke(cor_traco_preenchido)
            filho.set_stroke_weight(traco_preenchido)
        else:
            filho.set_fill(False)
            filho.set_stroke(cor)
            filho.set_stroke_weight(traco)
    py5.shape(forma)


def draw():
    py5.background(cor_fundo)
    paleta = gera_paleta("Okazz-230905a", True)
    with py5.push():
        py5.translate(0, 0, -150)
        for forma in formas:
            estiliza(forma, paleta[0])
            paleta.rotate(1)

    msg = (
        f"escala: {forma_escala:.2f} | altura: {altura:.0f} | "
        f"topo: {reducao_topo:.2f} | celulas: {len(formas)}"
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
    global forma_escala, preencher, jitter_bagunca
    global altura, reducao_topo, sombra_parede
    key = py5.key
    match key:
        case " ":
            save_and_close()
        case "r":
            inicializa()
        case "f":
            preencher = not preencher
        case "+" | "-":
            forma_escala = max(0.5, forma_escala + (0.05 if key == "+" else -0.05))
            inicializa()
        case "j" | "k":
            jitter_bagunca = max(0, jitter_bagunca + (5 if key == "j" else -5))
            inicializa()
        case "a" | "z":
            altura = max(0.0, altura + (5.0 if key == "a" else -5.0))
            inicializa()
        case "e" | "d":
            reducao_topo = min(
                1.0, max(0.30, reducao_topo + (0.05 if key == "e" else -0.05))
            )
            inicializa()
        case "s" | "x":
            sombra_parede = min(
                0.9, max(0.0, sombra_parede + (0.05 if key == "s" else -0.05))
            )


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
