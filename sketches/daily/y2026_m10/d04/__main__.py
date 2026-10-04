"""2026-10-04
Divisões redux 04
Inspirado em sketch de Alexandre Villares
ericof.com|https://abav.lugaralgum.com/sketch-a-day/#sketch_2026_02_16
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from dataclasses import dataclass
from dataclasses import field
from shapely import Polygon
from sketches.utils.draw import canvas
from sketches.utils.draw.cores import lerp_color_rgba
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
paleta: deque[int] = gera_paleta("azul", como_deque=True)

divisoes: int = 8
traco: int = 0


@dataclass
class InfoGrupo:
    vertices: list = field(default_factory=list)
    formas: list = field(default_factory=list)
    areas: list = field(default_factory=list)
    area_maxima: float = 0.0
    forma: py5.Py5Shape | None = None


grupos: dict[int, InfoGrupo] = {}

intensidade: float = 0.02
fator: float = 1.4
distorcao_va = 1.8


def cria_grupos(idx: int, largura: int, altura: int):
    """Initialize a division group from a rectangle covering the internal canvas."""
    vertices = [
        np.array(ponto)
        for ponto in ((0, 0), (largura, 0), (largura, altura), (0, altura))
    ]
    formas = []
    formas.append((0, 1, 2, 3))
    areas = [area_forma((0, 1, 2, 3), vertices)]
    grupos[idx] = InfoGrupo(
        forma=None,
        vertices=vertices,
        formas=formas,
        areas=areas,
        area_maxima=max(areas),
    )
    return grupos


def _divide_quadrado(
    idx: int, forma: tuple[int, ...], vertices: list, div: int = 2
) -> list[tuple[int, ...]]:
    """Divide a quadrilateral into triangles based on div.

    div=2: split along the shorter diagonal → 2 triangles, no new points.
    div=3: midpoint of the shorter diagonal added → 3 triangles; the two
           half-triangles each have area S/4 and the intact half has S/2
           (best achievable balance with a single added point).
    div=4: centroid added → 4 triangles, each S/4 for parallelograms and
           approximately equal for distorted quads.
    """
    a, b, c, d = forma
    ac = py5.dist(*vertices[a], *vertices[c])
    bd = py5.dist(*vertices[b], *vertices[d])
    gi = len(vertices)
    vertices.append((vertices[a] + vertices[b] + vertices[c] + vertices[d]) / gi)
    novas_formas = [(a, b, c), (a, c, d)] if ac < bd else [(a, b, d), (b, c, d)]
    match div:
        case 3:
            s = novas_formas.pop(-1)
            novas_formas.append((s[0], s[1], gi))
            novas_formas.append((gi, s[1], s[2]))
        case 4:
            novas_formas = [(a, b, gi), (b, c, gi), (c, d, gi), (d, a, gi)]
        case _:
            novas_formas = novas_formas
    print(f"{idx} - 4 -> {len(novas_formas)}")
    return novas_formas


def _divide_triangulo(
    idx: int, forma: tuple[int, ...], vertices: list, div: int = 2
) -> list[tuple[int, ...]]:
    """Divide a triangle into smaller triangles based on edge lengths."""
    a, b, c = forma
    ab = py5.dist(*vertices[a], *vertices[b])
    ab_m = (vertices[a] + vertices[b]) / div
    bc = py5.dist(*vertices[b], *vertices[c])
    bc_m = (vertices[b] + vertices[c]) / div
    ca = py5.dist(*vertices[c], *vertices[a])
    ca_m = (vertices[c] + vertices[a]) / div
    novas_formas = []
    if ab == bc == ca:
        bci = len(vertices)
        vertices.append(bc_m)
        novas_formas.append((a, b, bci))
        novas_formas.append((bci, a, c))
    elif ab == bc:
        cai = len(vertices)
        vertices.append(ca_m)
        novas_formas.append((a, b, cai))
        novas_formas.append((cai, a, c))
    elif bc == ca:
        abi = len(vertices)
        vertices.append(ab_m)
        novas_formas.append((a, c, abi))
        novas_formas.append((abi, b, c))
    else:
        novas_formas.append((a, c, b))
        novas_formas.append((b, a, c))
    print(f"{idx} - 3 -> {len(novas_formas)}")
    return novas_formas


DIVIDE_FORMA = {
    3: _divide_triangulo,
    4: _divide_quadrado,
}


def divide_formas(idx: int):
    """Create the next subdivision level for the given group index."""
    info = grupos.get(idx)
    if info and info.forma:
        # Não é necessário dividir novamente se já temos um grupo
        # para essa quantidade de divisões
        return
    idx_anterior = idx - 1 if idx > 1 else 1
    anterior = grupos[idx_anterior]
    formas = anterior.formas
    vertices = list(anterior.vertices)
    novas_formas = []
    while formas:
        forma = formas.pop()
        total = len(forma)
        div = 2 if total == 3 else py5.random_int(2, 4)
        funcao_divisao = DIVIDE_FORMA.get(total)
        if funcao_divisao:
            novas_formas.extend(funcao_divisao(idx, forma, vertices, div))

    areas = [area_forma(forma, vertices) for forma in novas_formas]
    info = InfoGrupo(
        forma=None,
        vertices=vertices,
        formas=novas_formas,
        areas=areas,
        area_maxima=max(areas),
    )
    grupos[idx] = info
    monta_grupo(idx)


def distorce(idx: int, intensidade=intensidade, fator=fator):
    """Apply radial distortion to the group's vertices based on center distance."""
    info = grupos[idx]
    vertices = info.vertices
    meio = helpers.DIMENSOES.internal[0] / 2, helpers.DIMENSOES.internal[1] / 2
    coordenadas = np.array(vertices)
    coordenadas -= np.array((meio[0], meio[1]))
    distancias = np.linalg.norm(coordenadas, axis=1)
    fatores_escala = 1 + (intensidade * (distancias**fator))
    coordenadas = distorcao_va * coordenadas / fatores_escala[:, np.newaxis]
    coordenadas += np.array(meio)
    info.vertices = coordenadas
    _monta_grupo(info)


def _monta_grupo(info: InfoGrupo):
    """Build and store a py5 group shape from an `InfoGrupo` definition."""
    grupo = py5.create_shape(py5.GROUP)
    formas = info.formas
    areas = info.areas
    vertices = info.vertices
    pares = list(zip(formas, areas, strict=False))
    for forma, _ in pares:
        poligono = py5.create_shape()
        cor = paleta[0]
        cor_proxima = paleta[1]
        pontos = np.array(vertices)[np.array(forma)]
        total = len(pontos)
        with poligono.begin_closed_shape():
            poligono.vertices(pontos)
        cores = []
        for i in range(total):
            cor = lerp_color_rgba(cor, cor_proxima, i, (0, total))
            cores.append(cor)
        poligono.set_fills(cores)
        poligono.set_stroke_weight(traco)
        grupo.add_child(poligono)
        paleta.rotate()
    info.forma = grupo


def monta_grupo(idx: int):
    """Create a renderable group shape for a stored subdivision group."""
    info = grupos[idx]
    if info.forma:
        # Já temos um shape para esse grupo, não precisamos recriar
        print(f"Shape para {idx} divisões já existe. Pulando criação.")
        return
    _monta_grupo(info)


def area_forma(forma, vertices):
    """Return the polygon area for a shape index tuple over a vertex list."""
    return Polygon(np.array(vertices)[np.array(forma)]).area


def inicializa():
    """Rebuild every subdivision level from 1 up to `divisoes`."""
    for idx in range(1, divisoes + 1):
        grupos = cria_grupos(idx, *helpers.DIMENSOES.internal)
        divide_formas(idx=idx)
        print(f"{idx} - {grupos[idx].forma.get_child_count()}")


def setup():
    """Configure the sketch and precompute subdivision groups up to `divisoes`."""
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    inicializa()


def draw():
    """Render the current subdivision group and update frame overlay metadata."""
    py5.background(cor_fundo)
    info = grupos[divisoes]
    if grupo := info.forma:
        with py5.push():
            py5.shape_mode(py5.CENTER)
            py5.translate(*helpers.DIMENSOES.centro)
            py5.shape(grupo)

    fps = py5.get_frame_rate()
    py5.window_title(f"Divisões: {divisoes} - Frame Rate: {fps:.2f}")
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def key_pressed():
    """Handle keyboard controls for saving, subdividing, and distortion."""
    global divisoes
    key = py5.key
    if key == " ":
        salva_e_encerra()
    elif key == "r":
        inicializa()
    elif key == "a":
        divisoes -= 1 if divisoes > 1 else 0
        divide_formas(divisoes)
    elif key == "d":
        divisoes += 1
        divide_formas(divisoes)
    elif key == "w":
        distorce(divisoes)


def salva_e_encerra():
    """Stop rendering, save the current frame, and exit the sketch."""
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
